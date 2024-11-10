from database import doctors, session


def add_doctor(name, seniority, age, category, image_url, description):
    insert_stmt = doctors.insert().values(
        dr_name=name,
        dr_seniority=seniority,
        dr_age=age,
        dr_category=category,
        dr_image_url=image_url,  # הוספת כתובת התמונה
        dr_description=description  # הוספת תיאור הרופא
    )
    session.execute(insert_stmt)
    session.commit()


def delete_doctor(doctor_id):
    delete_stmt = doctors.delete().where(doctors.c.dr_id == doctor_id)
    session.execute(delete_stmt)
    session.commit()


def update_doctor(doctor_id, name, seniority, age, category, image_url, description):
    update_stmt = doctors.update().where(doctors.c.dr_id == doctor_id).values(
        dr_name=name,
        dr_seniority=seniority,
        dr_age=age,
        dr_category=category,
        dr_image_url=image_url,  # עדכון כתובת התמונה
        dr_description=description  # עדכון תיאור הרופא
    )
    session.execute(update_stmt)
    session.commit()

