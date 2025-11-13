
from sqlalchemy import select, insert,delete
from datetime import datetime, date as date_cls
from database import Session, appointments, engine


def _coerce_date(value) -> date_cls:
    if isinstance(value, date_cls):
        return value
    s = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"bad date format: {value!r}")


def add_appointment(client_name, doctor_name, email, phone, date, message):
    values = {
        "client_name": (client_name or "").strip(),
        "doctor_name": (doctor_name or "").strip(),
        "email": (email or "").strip(),
        "phone": (phone or None),
        "date": _coerce_date(date),
        "message": (message or None),
    }


    with Session.begin() as session:
        session.execute(insert(appointments).values(**values))
    print("Appointment added successfully!")


def get_appointments(as_dict=True):

    with Session() as session:
        q = select(appointments).order_by(appointments.c.appointment_id.desc())
        res = session.execute(q)
        return res.mappings().all() if as_dict else res.fetchall()

def delete_appointment(appointment_id: int):
    with Session.begin() as session:
        session.execute(
            delete(appointments).where(appointments.c.appointment_id == appointment_id)
        )
    print(f"Appointment with ID {appointment_id} deleted successfully.")
