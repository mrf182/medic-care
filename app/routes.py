from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, flash, request, render_template, redirect, url_for, session as flask_session
from app.database import session as db_session, doctors, users
from app.models import (
    get_user_by_username, get_user_by_email, add_user, get_user_by_id,
    get_all_users_with_appointment_count, update_doctor, delete_doctor,
    add_doctor, add_appointment, get_appointments, delete_appointment
)
from werkzeug.security import generate_password_hash, check_password_hash


routes = Blueprint(
    "routes",
    __name__,
    template_folder="templates",
    static_folder="static"
)


@routes.route("/")
def index():
    doctors_list = db_session.query(doctors).all()
    return render_template("index.html", doctors=doctors_list)

@routes.route("/book", methods=["POST"])
def book():
    if not flask_session.get("user_id"):
        return jsonify({
            "success": False,
            "redirect": url_for("routes.login"),
            "message": "You must be logged in to book an appointment."
        }), 401

    add_appointment(
        request.form.get("name"),
        request.form.get("doctor_name"),
        request.form.get("email"),
        request.form.get("phone"),
        request.form.get("date"),
        request.form.get("message")
    )

    return jsonify({"success": True, "message": "The session was successfully saved"})

@routes.route("/delete_appointment/<int:appointment_id>", methods=["POST"])
def delete_appointment_route(appointment_id):
    delete_appointment(appointment_id)
    flash("The appointment was successfully deleted.", "success")
    return redirect(url_for("routes.admin_page"))

@routes.route("/doctor1/<int:doctor_id>")
def doctor1(doctor_id):
    doctor = db_session.query(doctors).filter(doctors.c.dr_id == doctor_id).first()
    if not doctor:
        return "Doctor not found", 404
    return render_template("doctor1.html", doctor=doctor)

@routes.route("/add_doctor", methods=["GET", "POST"])
def add_new_doctor():
    if request.method == "POST":
        add_doctor(
            request.form["name"],
            request.form["seniority"],
            request.form["age"],
            request.form["category"],
            request.form["image_url"],
            request.form["description"]
        )
        return redirect(url_for("routes.admin_page"))
    return render_template("add_doctor.html")

@routes.route("/delete_doctor/<int:doctor_id>", methods=["POST"])
def delete_doctor_route(doctor_id):
    delete_doctor(doctor_id)
    return redirect(url_for("routes.admin_page"))

@routes.route("/edit_doctor/<int:doctor_id>", methods=["GET", "POST"])
def edit_doctor_route(doctor_id):
    doctor = db_session.query(doctors).filter(doctors.c.dr_id == doctor_id).first()
    if request.method == "POST":
        update_doctor(
            doctor_id,
            request.form["name"],
            request.form["seniority"],
            request.form["age"],
            request.form["category"],
            request.form["image_url"],
            request.form["description"]
        )
        return redirect(url_for("routes.admin_page"))
    return render_template("edit_doctor.html", doctor=doctor)

@routes.route("/admin")
def admin_page():
    if flask_session.get("is_admin"):
        return render_template(
            "admin.html",
            doctors=db_session.query(doctors).all(),
            appointments=get_appointments(),
            users=get_all_users_with_appointment_count()
        )
    return redirect(url_for("routes.login"))

@routes.route("/login", methods=["GET", "POST"])
def login():
    username_error = password_error = blocked_error = False

    if request.method == "POST":
        username = request.form.get("username")
        password_input = request.form.get("password")

        if username == "admin" and password_input == "123456":
            flask_session["is_admin"] = True
            return redirect(url_for("routes.admin_page"))

        user = get_user_by_username(username)

        if user:
            if user["is_blocked"]:
                blocked_error = True
            elif not check_password_hash(user["password"], password_input):
                password_error = True
            else:
                flask_session["user_id"] = user["id"]
                return redirect(url_for("routes.index"))
        else:
            username_error = True

        return render_template(
            "login.html",
            username=username,
            username_error=username_error,
            password_error=password_error,
            blocked_error=blocked_error
        )

    return render_template("login.html")

@routes.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    if not username or not password or not email:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    if get_user_by_username(username):
        return jsonify({"success": False, "message": "Username already exists."}), 400
    if get_user_by_email(email):
        return jsonify({"success": False, "message": "Email already exists."}), 400

    try:
        add_user(username, password, email)
        db_session.commit()
        return jsonify({"success": True, "message": "Registration successful!"})
    except IntegrityError:
        db_session.rollback()
        return jsonify({"success": False, "message": "Email or username already exists."}), 400
    except Exception:
        db_session.rollback()
        return jsonify({"success": False, "message": "Unexpected server error."}), 500

@routes.route("/register", methods=["GET"])
def register_form():
    return render_template("register.html")

@routes.route("/toggle_block_user/<int:user_id>", methods=["POST"])
def toggle_block_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        db_session.execute(users.update().where(users.c.id == user_id).values(is_blocked=not user.is_blocked))
        db_session.commit()
    return redirect(url_for("routes.admin_page"))

@routes.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    db_session.execute(users.delete().where(users.c.id == user_id))
    db_session.commit()
    return redirect(url_for("routes.admin_page"))
