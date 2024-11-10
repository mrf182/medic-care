from sqlalchemy import select

from database import Session, appointments, engine


def add_appointment(client_name, doctor_name, email, phone, date, message):
    # יצירת סשן חדש
    session = Session()
    try:
        # הוספת הרשומה לסשן
        insert_stmt = appointments.insert().values(
            client_name=client_name,
            doctor_name=doctor_name,
            email=email,
            phone=phone,
            date=date,
            message=message
        )
        session.execute(insert_stmt)
        # שמירת השינויים במסד הנתונים
        session.commit()
        print("Appointment added successfully!")  # הודעה להדפסה
    except Exception as e:
        session.rollback()  # אם יש שגיאה, החזר את השינויים
        print(f"Error adding appointment: {e}")  # טיפול בשגיאות
    finally:
        session.close()  # סגירת הסשן


# פונקציה לשליפת רשימת הפגישות
def get_appointments():
    try:
        select_stmt = select([appointments])
        with engine.connect() as conn:
            result = conn.execute(select_stmt)
            appointments_list = result.fetchall()
        return appointments_list
    except Exception as e:
        print(f"Error retrieving appointments: {e}")
        return []
