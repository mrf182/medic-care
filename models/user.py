from werkzeug.security import generate_password_hash
from sqlalchemy import func, select
from database import session, users, appointments


from datetime import datetime

def add_user(username, password, email):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    insert_stmt = users.insert().values(
        username=username,
        password=hashed_password,
        email=email,
        join_date=datetime.utcnow()
    )
    session.execute(insert_stmt)
    session.commit()

def get_user_by_username(username):
    select_stmt = users.select().where(users.c.username == username)
    result = session.execute(select_stmt).mappings().fetchone()
    return result



def get_user_by_email(user_email):
    select_stmt = users.select().where(users.c.username == user_email)
    return session.execute(select_stmt).fetchone()

def get_user_by_id(user_id):
    select_stmt = users.select().where(users.c.id == user_id)
    return session.execute(select_stmt).fetchone()


def get_all_users_with_appointment_count():
    stmt = (
        select(
            users.c.id,
            users.c.username,
            users.c.email,
            users.c.phone,
            users.c.is_blocked,
            users.c.join_date,
            func.count(appointments.c.appointment_id).label("appointment_count")
        )
        .select_from(users.outerjoin(appointments, users.c.email == appointments.c.email))
        .group_by(
            users.c.id,
            users.c.username,
            users.c.phone,
            users.c.email,
            users.c.is_blocked,
            users.c.join_date
        )
    )
    return session.execute(stmt).fetchall()


