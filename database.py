from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Date, select, Boolean
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

DATABASE_URI = (
    "mssql+pyodbc://@localhost\\SQLEXPRESS/python_data"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&Trusted_Connection=yes"
)

engine = create_engine(DATABASE_URI, future=True)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData(schema="dbo")

# טבלת הרופאים כולל עמודת התמונה
doctors = Table('doctors', metadata,
                Column('dr_id', Integer, primary_key=True),
                Column('dr_name', String(50), nullable=False),
                Column('dr_seniority', Integer),
                Column('dr_age', Integer),
                Column('dr_category', String(50)),
                Column('dr_image_url', String(255)),  # עמודה לתמונה
                Column('dr_description', Text))  # עמודה לתיאור הרופא

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String(50), nullable=False, unique=True),
              Column('password', String(255), nullable=False),  # Plain password
              Column('email', String(100), nullable=False, unique=True),
              Column('is_robot', Boolean, default=False))  # Robot check column

metadata.create_all(engine)

# טבלת הפגישות
appointments = Table('appointments', metadata,
                     Column('appointment_id', Integer, primary_key=True),
                     Column('client_name', String(100), nullable=False),
                     Column('doctor_name', String(50), nullable=False),
                     Column('email', String(100), nullable=False),
                     Column('phone', String(20)),
                     Column('date', Date, nullable=False),
                     Column('message', Text))

# יצירת הטבלאות במסד הנתונים (במידה והן לא קיימות)
metadata.create_all(engine)


