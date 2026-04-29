from datetime import datetime

from clinic.models import DoctorAvailability
from clinic.repositories import ClinicRepository


class AvailabilityService:
    def __init__(self, repository=None):
        self.repository = repository or ClinicRepository()

    def create_availability(self, form_data, doctor_id):
        errors = self._validate_form(form_data)
        if errors:
            return None, errors

        start_time = datetime.strptime(form_data["start_time"], "%H:%M").time()
        end_time = datetime.strptime(form_data["end_time"], "%H:%M").time()
        if end_time <= start_time:
            return None, ["End time must be later than start time."]

        availability = DoctorAvailability(
            doctor_id=doctor_id,
            available_date=datetime.strptime(form_data["available_date"], "%Y-%m-%d").date(),
            start_time=start_time,
            end_time=end_time,
            slot_minutes=int(form_data.get("slot_minutes", 30)),
            status=form_data.get("status", "available"),
            note=form_data.get("note"),
        )
        self.repository.add_availability(availability)
        self.repository.commit()
        return availability, []

    def _validate_form(self, form_data):
        required_fields = ["available_date", "start_time", "end_time", "slot_minutes"]
        missing = [field for field in required_fields if not form_data.get(field)]
        if missing:
            return ["Please fill in all required availability fields."]
        return []
