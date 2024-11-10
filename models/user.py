from werkzeug.security import generate_password_hash

from database import users, session


def add_user(username, password, email, ):
    hashed_password = generate_password_hash(password)
    insert_stmt = users.insert().values(
        username=username,
        password=hashed_password,
        email=email,

    )
    session.execute(insert_stmt)
    session.commit()

def get_user_by_username(username):
    select_stmt = users.select().where(users.c.username == username)
    return session.execute(select_stmt).fetchone()

def get_user_by_email(user_email):
    select_stmt = users.select().where(users.c.username == user_email)
    return session.execute(select_stmt).fetchone()

def get_user_by_id(user_id):
    select_stmt = users.select().where(users.c.id == user_id)
    return session.execute(select_stmt).fetchone()


def get_user_by_password(password):
    select_stmt = users.select().where(users.c.password == password)
    return session.execute(select_stmt).fetchone()
