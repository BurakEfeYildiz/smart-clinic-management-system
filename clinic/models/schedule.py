from clinic.extensions import db


class DoctorAvailability(db.Model):
    __tablename__ = "doctor_availabilities"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_profiles.id"), nullable=False)
    available_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    slot_minutes = db.Column(db.Integer, nullable=False, default=30)
    status = db.Column(db.String(30), nullable=False, default="available")
    note = db.Column(db.String(180), nullable=True)

    doctor = db.relationship("DoctorProfile", back_populates="availabilities")

    __table_args__ = (
        db.CheckConstraint("end_time > start_time", name="ck_availability_time_range"),
    )
