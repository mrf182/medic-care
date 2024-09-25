import os
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
from database import update_doctor, delete_doctor, add_doctor, doctors, session
import logging

app = Flask(__name__)

# הגדרת תיקייה להעלאת קבצים
UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# הגדרת רמות הלוגים
logging.basicConfig(level=logging.DEBUG)

# פונקציה לבדוק אם הסיומת מותרת
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    doctors_list = session.query(doctors).all()  # מחזיר את כל הרופאים מהטבלה
    return render_template("index.html", doctors=doctors_list)  # מעביר את הרשימה לעמוד

@app.route("/doctor1")
def doctor1():
    return render_template("doctor1.html")

@app.route("/doctor2")
def doctor2():
    return render_template("doctor2.html")

@app.route("/doctor3")
def doctor3():
    return render_template("doctor3.html")

@app.route("/doctor4")
def doctor4():
    return render_template("doctor3.html")

# הוספת רופא
@app.route("/add_doctor", methods=["GET", "POST"])
def add_new_doctor():
    if request.method == "POST":
        name = request.form["name"]
        seniority = request.form["seniority"]
        age = request.form["age"]
        category = request.form["category"]
        image_url = request.form["image_url"]  # קבלת ה-URL מהשדה

        # הוספת רופא למסד הנתונים
        add_doctor(name, seniority, age, category, image_url)
        return redirect(url_for("index"))  # הפנייה לעמוד הראשי
    return render_template("add_doctor.html")

# מחיקת רופא
@app.route("/delete_doctor/<int:doctor_id>", methods=["POST"])
def delete_doctor_route(doctor_id):
    delete_doctor(doctor_id)  # קריאה לפונקציה למחיקת רופא
    return redirect(url_for("index"))  # הפנה לעמוד הראשי

# עריכת רופא
@app.route("/edit_doctor/<int:doctor_id>", methods=["GET", "POST"])
def edit_doctor_route(doctor_id):
    doctor = session.query(doctors).filter(doctors.c.dr_id == doctor_id).first()  # מציאת הרופא
    if request.method == "POST":
        name = request.form["name"]
        seniority = request.form["seniority"]
        age = request.form["age"]
        category = request.form["category"]
        image_url = request.form["image_url"]  # עדכון ה-URL שנכנס מהטופס

        update_doctor(doctor_id, name, seniority, age, category, image_url)  # עדכון הרופא במסד הנתונים
        return redirect(url_for("index"))
    return render_template("edit_doctor.html", doctor=doctor)  # מעביר את פרטי הרופא לתבנית


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # קבלת שם המשתמש והסיסמה מהטופס
        username = request.form.get("username")
        password = request.form.get("password")

        # בדיקה אם שם המשתמש והסיסמה נכונים
        if username == "admin" and password == "123456":
            # שליפת כל הרופאים מה-DB
            doctors = Doctor.query.all()
            # הפניה לעמוד admin.html עם רשימת הרופאים
            return render_template("admin.html", doctors=doctors)
        else:
            return redirect(url_for("index"))  # הפניה לעמוד index.html אם לא מנהל

    return render_template("login.html")  # הצגת עמוד ההתחברות אם הבקשה היא GET

port_number = 3000
if __name__ == '__main__':
    app.run(port=port_number)
