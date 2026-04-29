from clinic.extensions import db


class DoctorProfile(db.Model):
    __tablename__ = "doctor_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    title = db.Column(db.String(80), nullable=False, default="Doctor")
    room_number = db.Column(db.String(30), nullable=True)

    user = db.relationship("User", back_populates="doctor_profile")
    department = db.relationship("Department", back_populates="doctors")
    availabilities = db.relationship("DoctorAvailability", back_populates="doctor")
    appointments = db.relationship("Appointment", back_populates="doctor")
