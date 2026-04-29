from datetime import datetime

from clinic.extensions import db


class PatientFlow(db.Model):
    __tablename__ = "patient_flow"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"), nullable=True)
    current_status = db.Column(db.String(30), nullable=False, default="waiting")
    queue_number = db.Column(db.Integer, nullable=True)
    checked_in_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    patient = db.relationship("Patient", back_populates="flow_records")
    appointment = db.relationship("Appointment", back_populates="flow_record")
