# models/doctor.py
import os
import re
import uuid
import base64
from typing import Optional
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from app.database import doctors, session  # חשוב: doctors הוא Table מתוך MetaData(schema="dbo") אם יש


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _to_int_or_none(v) -> Optional[int]:
    if v is None:
        return None
    if isinstance(v, int):
        return v
    s = str(v).strip()
    return int(s) if s else None


def _to_str_or_none(v) -> Optional[str]:
    if v is None:
        return None
    s = str(v).strip()
    return s if s else None


DATA_URI_RE = re.compile(r"^data:image/(png|jpeg|jpg);base64,(.+)$", re.IGNORECASE)


def _store_data_uri_if_needed(image_value: Optional[str]) -> Optional[str]:

    if not image_value:
        return None
    m = DATA_URI_RE.match(image_value)
    if not m:

        return image_value

    ext = m.group(1).lower()
    ext = "jpg" if ext in ("jpeg", "jpg") else "png"
    raw = m.group(2)

    try:
        blob = base64.b64decode(raw)
    except Exception:

        return None

    fname = f"{uuid.uuid4().hex}.{ext}"
    fpath = os.path.join(UPLOAD_DIR, fname)
    with open(fpath, "wb") as f:
        f.write(blob)


    return f"/static/uploads/{fname}"


def add_doctor(name, seniority, age, category, image_url, description):
    values = {
        "dr_name": _to_str_or_none(name),
        "dr_seniority": _to_int_or_none(seniority),
        "dr_age": _to_int_or_none(age),
        "dr_category": _to_str_or_none(category),
        "dr_image_url": _store_data_uri_if_needed(_to_str_or_none(image_url)),
        "dr_description": _to_str_or_none(description),
    }

    try:
        session.execute(insert(doctors).values(**values))
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise


def delete_doctor(doctor_id):
    try:
        session.execute(delete(doctors).where(doctors.c.dr_id == _to_int_or_none(doctor_id)))
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise


def update_doctor(doctor_id, name, seniority, age, category, image_url, description):

    to_set = {
        "dr_name": _to_str_or_none(name),
        "dr_seniority": _to_int_or_none(seniority),
        "dr_age": _to_int_or_none(age),
        "dr_category": _to_str_or_none(category),
        "dr_description": _to_str_or_none(description),
    }

    img = _to_str_or_none(image_url)
    if img is not None and img != "":
        to_set["dr_image_url"] = _store_data_uri_if_needed(img)

    to_set = {k: v for k, v in to_set.items() if v is not None}

    try:
        session.execute(
            update(doctors)
            .where(doctors.c.dr_id == _to_int_or_none(doctor_id))
            .values(**to_set)
        )
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
