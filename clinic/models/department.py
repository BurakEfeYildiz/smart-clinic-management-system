from clinic.extensions import db


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    floor = db.Column(db.String(40), nullable=True)
    description = db.Column(db.Text, nullable=True)

    doctors = db.relationship("DoctorProfile", back_populates="department")
