from datetime import date, time, timedelta

from clinic.extensions import db
from clinic.models import Department, DoctorAvailability, DoctorProfile, Patient, User


def register_commands(app):
    @app.cli.command("init-db")
    def init_db():
        db.drop_all()
        db.create_all()

        cardiology = Department(name="Cardiology", floor="2nd Floor")
        dermatology = Department(name="Dermatology", floor="3rd Floor")
        db.session.add_all([cardiology, dermatology])

        secretary = User(
            full_name="Aylin Demir",
            username="aylin.demir",
            email="secretary@clinic.local",
            phone="+90 555 100 2025",
            employee_code="SEC-204",
            role="secretary",
        )
        secretary.set_password("clinic123")

        patient_user = User(
            full_name="Mert Kaya",
            username="mert.kaya",
            email="patient@clinic.local",
            phone="+90 555 100 2026",
            role="patient",
        )
        patient_user.set_password("clinic123")

        doctor_user = User(
            full_name="Dr. Deniz Arslan",
            username="deniz.arslan",
            email="doctor@clinic.local",
            phone="+90 555 100 2027",
            employee_code="DOC-204",
            role="doctor",
        )
        doctor_user.set_password("clinic123")
        db.session.add_all([secretary, patient_user, doctor_user])
        db.session.flush()

        doctor = DoctorProfile(
            user_id=doctor_user.id,
            department=cardiology,
            title="Cardiologist",
            room_number="204",
        )
        db.session.add(doctor)
        db.session.flush()

        patient = Patient(
            national_id="12345678910",
            full_name="Mert Kaya",
            phone="+90 555 100 2026",
            email="patient@clinic.local",
        )
        db.session.add(patient)

        today = date.today()
        for offset in range(5):
            db.session.add(
                DoctorAvailability(
                    doctor_id=doctor.id,
                    available_date=today + timedelta(days=offset),
                    start_time=time(9, 0),
                    end_time=time(16, 0),
                    slot_minutes=30,
                    status="available",
                )
            )

        db.session.commit()
        print("Database initialized with demo clinic data.")
