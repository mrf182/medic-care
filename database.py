from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST

# הגדרת מחרוזת החיבור
DATABASE_URI = 'mssql+pyodbc://@DESKTOP-24EQMFH/python_data?driver=SQL+Server&Trusted_Connection=yes'

engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()

# טבלת הרופאים
# טבלת הרופאים כולל עמודת התמונה
doctors = Table('doctors', metadata,
                Column('dr_id', Integer, primary_key=True),
                Column('dr_name', String(50), nullable=False),
                Column('dr_seniority', Integer),
                Column('dr_age', Integer),
                Column('dr_category', String(50)),
                Column('dr_image_url', String(255)))  # עמודה לתמונה

metadata.create_all(engine)

# פונקציות CRUD (הוספה, מחיקה, עדכון)
def add_doctor(name, seniority, age, category, image_url):
    insert_stmt = doctors.insert().values(
        dr_name=name,
        dr_seniority=seniority,
        dr_age=age,
        dr_category=category,
        dr_image_url=image_url  # הוספת כתובת התמונה
    )
    session.execute(insert_stmt)
    session.commit()


def delete_doctor(doctor_id):
    delete_stmt = doctors.delete().where(doctors.c.dr_id == doctor_id)
    session.execute(delete_stmt)
    session.commit()

def update_doctor(doctor_id, name, seniority, age, category, image_url):
    update_stmt = doctors.update().where(doctors.c.dr_id == doctor_id).values(
        dr_name=name,
        dr_seniority=seniority,
        dr_age=age,
        dr_category=category,
        dr_image_url=image_url  # עדכון כתובת התמונה
    )
    session.execute(update_stmt)
    session.commit()
