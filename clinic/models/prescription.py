from datetime import datetime

from clinic.extensions import db


class Prescription(db.Model):
    __tablename__ = "prescriptions"

    id = db.Column(db.Integer, primary_key=True)
    medical_record_id = db.Column(db.Integer, db.ForeignKey("medical_records.id"), nullable=False)
    medication_name = db.Column(db.String(140), nullable=False)
    dosage = db.Column(db.String(120), nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
