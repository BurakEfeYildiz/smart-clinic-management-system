from datetime import datetime

from clinic.models import Appointment, PatientFlow
from clinic.repositories import ClinicRepository
from clinic.services.time_slots import build_time_slots


class AppointmentService:
    def __init__(self, repository=None):
        self.repository = repository or ClinicRepository()

    def create_appointment(self, form_data, created_by_user_id=None):
        errors = self._validate_form(form_data)
        if errors:
            return None, errors

        doctor_id = int(form_data["doctor_id"])
        appointment_date = datetime.strptime(form_data["appointment_date"], "%Y-%m-%d").date()
        appointment_time = datetime.strptime(form_data["appointment_time"], "%H:%M").time()

        if self.repository.find_appointment_slot(doctor_id, appointment_date, appointment_time):
            return None, ["This doctor already has an appointment at the selected time."]

        if not self._slot_is_available(doctor_id, appointment_date, appointment_time):
            return None, ["The selected time is outside the doctor's available schedule."]

        patient = self.repository.get_or_create_patient(
            {
                "national_id": form_data["national_id"],
                "full_name": form_data["patient_name"],
                "phone": form_data.get("phone"),
                "email": form_data.get("email"),
                "birth_date": None,
                "gender": form_data.get("gender"),
                "address": None,
                "emergency_contact": None,
            }
        )
        appointment = Appointment(
            patient=patient,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=form_data["reason"].strip(),
            created_by_user_id=created_by_user_id,
        )
        self.repository.add_appointment(appointment)
        self.repository.commit()
        return appointment, []

    def available_slots_for_doctor(self, doctor_id, appointment_date):
        availabilities = self.repository.list_doctor_availability(doctor_id, appointment_date)
        appointments = self.repository.list_appointments(doctor_id, appointment_date)
        booked = {item.appointment_time for item in appointments if item.status != "cancelled"}

        slots = []
        for availability in availabilities:
            for slot in build_time_slots(
                availability.start_time,
                availability.end_time,
                availability.slot_minutes,
            ):
                slots.append(
                    {
                        "time": slot,
                        "is_available": availability.status == "available" and slot not in booked,
                        "is_booked": slot in booked,
                    }
                )
        return slots

    def check_in_appointment(self, appointment_id):
        appointment = self.repository.get_appointment(appointment_id)
        if not appointment:
            return None, ["Appointment could not be found."]
        if appointment.flow_record:
            return appointment.flow_record, []

        flow_record = PatientFlow(
            patient_id=appointment.patient_id,
            appointment_id=appointment.id,
            current_status="waiting",
            queue_number=self.repository.next_queue_number(),
        )
        appointment.status = "checked_in"
        self.repository.add_patient_flow(flow_record)
        self.repository.commit()
        return flow_record, []

    def _slot_is_available(self, doctor_id, appointment_date, appointment_time):
        availabilities = self.repository.list_doctor_availability(doctor_id, appointment_date)
        for availability in availabilities:
            if (
                availability.status == "available"
                and availability.start_time <= appointment_time < availability.end_time
            ):
                return True
        return False

    def _validate_form(self, form_data):
        required_fields = [
            "national_id",
            "patient_name",
            "doctor_id",
            "appointment_date",
            "appointment_time",
            "reason",
        ]
        missing = [field for field in required_fields if not form_data.get(field)]
        if missing:
            return ["Please fill in all required appointment fields."]
        return []
