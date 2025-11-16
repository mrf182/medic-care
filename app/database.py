from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Date, select, Boolean, DateTime
from sqlalchemy.orm import sessionmaker


DATABASE_URI = (
     "sqlite:///mydb.sqlite3"

)

engine = create_engine(DATABASE_URI, future=True)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()



doctors = Table('doctors', metadata,
                Column('dr_id', Integer, primary_key=True),
                Column('dr_name', String(50), nullable=False),
                Column('dr_seniority', Integer),
                Column('dr_age', Integer),
                Column('dr_category', String(50)),
                Column('dr_image_url', String(255)),
                Column('dr_description', Text))

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String(50), nullable=False, unique=True),
              Column('password', String(255), nullable=False),
              Column('email', String(100), nullable=False, unique=True),
              Column('is_blocked', Boolean, default=False),
              Column('phone', String(11), default=False),
              Column('join_date', DateTime, default=datetime.utcnow))




metadata.create_all(engine)


appointments = Table('appointments', metadata,
                     Column('appointment_id', Integer, primary_key=True),
                     Column('client_name', String(100), nullable=False),
                     Column('doctor_name', String(50), nullable=False),
                     Column('email', String(100), nullable=False),
                     Column('phone', String(20)),
                     Column('date', Date, nullable=False),
                     Column('message', Text))


metadata.create_all(engine)


