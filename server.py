
from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, request, url_for, redirect, session as flask_session, jsonify, flash
from werkzeug.security import check_password_hash, generate_password_hash
from database import session as db_session, doctors, users
from models.user import get_user_by_username, get_user_by_email, add_user, get_user_by_id, \
    get_all_users_with_appointment_count
from models.doctor import update_doctor, delete_doctor, add_doctor
from models.appointment import add_appointment, get_appointments, delete_appointment
from flask import request, render_template, redirect, url_for, session as flask_session
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route("/")
def index():
    doctors_list = db_session.query(doctors).all()
    password_plain = "ת"
    hashed = generate_password_hash(password_plain, method='pbkdf2:sha256', salt_length=16)

    print(f"hashed: {hashed}")
    print("האם תואם?", check_password_hash(hashed, password_plain))
    return render_template("index.html", doctors=doctors_list)





@app.route("/book", methods=["POST"])
def book():
    if not flask_session.get("user_id"):
        return jsonify({
            "success": False,
            "redirect": url_for("login"),
            "message": "You must be logged in to book an appointment."
        }), 401


    client_name = request.form.get("name")
    doctor_name = request.form.get("doctor_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    date = request.form.get("date")
    message = request.form.get("message")

    add_appointment(client_name, doctor_name, email, phone, date, message)

    return jsonify({"success": True, "message": "The session was successfully saved"})

@app.route("/delete_appointment/<int:appointment_id>", methods=["POST"])
def delete_appointment_route(appointment_id):
    delete_appointment(appointment_id)
    flash("The appointment was successfully deleted.", "success")
    return redirect(url_for("admin_page"))

@app.route("/doctor1/<int:doctor_id>")
def doctor1(doctor_id):
    doctor = db_session.query(doctors).filter(doctors.c.dr_id == doctor_id).first()
    if not doctor:
        return "Doctor not found", 404
    return render_template("doctor1.html", doctor=doctor)

@app.route("/add_doctor", methods=["GET", "POST"])
def add_new_doctor():
    if request.method == "POST":
        name = request.form["name"]
        seniority = request.form["seniority"]
        age = request.form["age"]
        category = request.form["category"]
        image_url = request.form["image_url"]
        description = request.form["description"]


        add_doctor(name, seniority, age, category, image_url, description)
        return redirect(url_for("admin_page"))
    return render_template("add_doctor.html")

@app.route("/delete_doctor/<int:doctor_id>", methods=["POST"])
def delete_doctor_route(doctor_id):
    delete_doctor(doctor_id)
    return redirect(url_for("admin_page"))

@app.route("/edit_doctor/<int:doctor_id>", methods=["GET", "POST"])
def edit_doctor_route(doctor_id):
    doctor = db_session.query(doctors).filter(doctors.c.dr_id == doctor_id).first()
    if request.method == "POST":
        name = request.form["name"]
        seniority = request.form["seniority"]
        age = request.form["age"]
        category = request.form["category"]
        image_url = request.form["image_url"]
        description = request.form["description"]

        update_doctor(doctor_id, name, seniority, age, category, image_url, description)
        return redirect(url_for("admin_page"))
    return render_template("edit_doctor.html", doctor=doctor)

@app.route("/admin")
def admin_page():
    if flask_session.get("is_admin"):
        doctors_list = db_session.query(doctors).all()
        appointments_list = get_appointments()
        users_list = get_all_users_with_appointment_count()
        return render_template("admin.html", doctors=doctors_list, appointments=appointments_list, users=users_list)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    username_error = False
    password_error = False
    blocked_error = False

    if request.method == "POST":
        username = request.form.get("username")
        password_input = request.form.get("password")

        if username == "admin" and password_input == "123456":
            flask_session["is_admin"] = True
            return redirect(url_for("admin_page"))

        user = get_user_by_username(username)

        if user:

            stored_hash = user["password"]
            hash_method = stored_hash.split(":")[0] if ":" in stored_hash else "unknown"


            if user["is_blocked"]:
                blocked_error = True

            elif not check_password_hash(stored_hash, password_input):
                password_error = True

            else:
                flask_session["user_id"] = user["id"]
                return redirect(url_for("index"))

        else:
            username_error = True
            username = ""

        return render_template("login.html",
                               username=username,
                               username_error=username_error,
                               password_error=password_error,
                               blocked_error=blocked_error)

    return render_template("login.html",
                           username_error=username_error,
                           password_error=password_error)


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    if not username or not password or not email:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    if get_user_by_username(username):
        return jsonify({
            "success": False,
            "message": "Username already exists. Please choose another one."
        }), 400

    if get_user_by_email(email):
        return jsonify({
            "success": False,
            "message": "Email is already registered. Please login or use another email."
        }), 400

    try:
        add_user(username, password, email)
        db_session.commit()

        return jsonify({
            "success": True,
            "message": "Registration successful!"
        })

    except IntegrityError as e:

        db_session.rollback()

        return jsonify({

            "success": False,

            "message": "Email or username already exists."

        }), 400

    except Exception as e:
        db_session.rollback()
        return jsonify({
            "success": False,
            "message": "Unexpected server error. Please try again later."
        }), 500

@app.route("/register", methods=["GET"])
def register_form():
    return render_template("register.html")

@app.route("/toggle_block_user/<int:user_id>", methods=["POST"])
def toggle_block_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        new_status = not user.is_blocked
        db_session.execute(users.update().where(users.c.id == user_id).values(is_blocked=new_status))
        db_session.commit()
    return redirect(url_for("admin_page"))

@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    db_session.execute(users.delete().where(users.c.id == user_id))
    db_session.commit()
    return redirect(url_for("admin_page"))

port_number = 3000
if __name__ == '__main__':
    app.run(port=port_number)