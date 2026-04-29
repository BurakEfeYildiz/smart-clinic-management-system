from datetime import date

from clinic.extensions import db
from clinic.models import (
    Appointment,
    Department,
    DoctorAvailability,
    DoctorProfile,
    Patient,
    PatientFlow,
    User,
)


class ClinicRepository:
    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def list_users_by_role(self, role):
        return User.query.filter_by(role=role).order_by(User.full_name).all()

    def get_user(self, user_id):
        return db.session.get(User, user_id)

    def list_departments(self):
        return Department.query.order_by(Department.name).all()

    def get_department(self, department_id):
        return db.session.get(Department, department_id)

    def list_doctors(self):
        return DoctorProfile.query.join(User).order_by(User.full_name).all()

    def get_doctor(self, doctor_id):
        return db.session.get(DoctorProfile, doctor_id)

    def get_patient(self, patient_id):
        return db.session.get(Patient, patient_id)

    def get_or_create_patient(self, patient_data):
        national_id = patient_data["national_id"].strip()
        patient = Patient.query.filter_by(national_id=national_id).first()
        if patient:
            patient.full_name = patient_data["full_name"].strip()
            patient.phone = patient_data.get("phone")
            patient.email = patient_data.get("email")
            return patient

        patient = Patient(
            national_id=national_id,
            full_name=patient_data["full_name"].strip(),
            birth_date=patient_data.get("birth_date"),
            gender=patient_data.get("gender"),
            phone=patient_data.get("phone"),
            email=patient_data.get("email"),
            address=patient_data.get("address"),
            emergency_contact=patient_data.get("emergency_contact"),
        )
        db.session.add(patient)
        return patient

    def list_patients(self):
        return Patient.query.order_by(Patient.full_name).all()

    def list_appointments(self, doctor_id=None, patient_email=None, appointment_date=None):
        query = Appointment.query
        if doctor_id:
            query = query.filter_by(doctor_id=doctor_id)
        if patient_email:
            query = query.join(Patient).filter(Patient.email == patient_email)
        if appointment_date:
            query = query.filter_by(appointment_date=appointment_date)
        return query.order_by(Appointment.appointment_date, Appointment.appointment_time).all()

    def get_appointment(self, appointment_id):
        return db.session.get(Appointment, appointment_id)

    def find_appointment_slot(self, doctor_id, appointment_date, appointment_time):
        return Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
        ).first()

    def list_doctor_availability(self, doctor_id=None, available_date=None):
        query = DoctorAvailability.query
        if doctor_id:
            query = query.filter_by(doctor_id=doctor_id)
        if available_date:
            query = query.filter_by(available_date=available_date)
        return query.order_by(DoctorAvailability.available_date, DoctorAvailability.start_time).all()

    def add_availability(self, availability):
        db.session.add(availability)
        return availability

    def add_appointment(self, appointment):
        db.session.add(appointment)
        return appointment

    def add_user(self, user):
        db.session.add(user)
        return user

    def add_patient(self, patient):
        db.session.add(patient)
        return patient

    def add_doctor_profile(self, doctor_profile):
        db.session.add(doctor_profile)
        return doctor_profile

    def add_patient_flow(self, flow_record):
        db.session.add(flow_record)
        return flow_record

    def get_flow_record(self, flow_id):
        return db.session.get(PatientFlow, flow_id)

    def list_patient_flow(self):
        return (
            PatientFlow.query.order_by(
                PatientFlow.checked_in_at.desc(),
                PatientFlow.queue_number.asc(),
            )
            .limit(50)
            .all()
        )

    def next_queue_number(self):
        latest = (
            PatientFlow.query.filter(PatientFlow.checked_in_at >= date.today())
            .order_by(PatientFlow.queue_number.desc())
            .first()
        )
        if not latest or latest.queue_number is None:
            return 1
        return latest.queue_number + 1

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def flush(self):
        db.session.flush()
