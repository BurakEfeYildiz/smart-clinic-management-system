from clinic.models import DoctorProfile, Patient, User
from clinic.repositories import ClinicRepository


class AuthService:
    VALID_ROLES = {"patient", "doctor", "secretary"}

    def __init__(self, repository=None):
        self.repository = repository or ClinicRepository()

    def login(self, username, password):
        if not username or not password:
            return None, ["Please enter both username and password."]

        user = self.repository.get_user_by_username(username.strip())
        if not user:
            return None, ["The username could not be found."]

        if not user.check_password(password):
            return None, ["The password you entered is incorrect."]

        return user, []

    def register(self, form_data):
        role = (form_data.get("role") or "").strip()
        username = (form_data.get("username") or "").strip()
        email = (form_data.get("email") or "").strip().lower()
        employee_code = self._employee_code(form_data, role)
        errors = self._validate_registration(form_data)
        if errors:
            return None, errors

        if self.repository.get_user_by_username(username):
            return None, ["This username is already in use."]

        if self.repository.get_user_by_email(email):
            return None, ["This email address is already registered."]

        user = User(
            full_name=form_data["full_name"].strip(),
            username=username,
            email=email,
            phone=(form_data.get("phone") or "").strip() or None,
            employee_code=employee_code,
            role=role,
        )
        user.set_password(form_data["password"])
        self.repository.add_user(user)
        self.repository.flush()

        if role == "patient":
            patient = Patient(
                national_id=form_data["national_id"].strip(),
                full_name=user.full_name,
                gender=(form_data.get("gender") or "").strip() or None,
                phone=user.phone,
                email=user.email,
            )
            self.repository.add_patient(patient)
        elif role == "doctor":
            doctor_profile = DoctorProfile(
                user_id=user.id,
                department_id=int(form_data["department_id"]),
                title=(form_data.get("title") or "").strip() or "Doctor",
                room_number=(form_data.get("room_number") or "").strip() or None,
            )
            self.repository.add_doctor_profile(doctor_profile)

        self.repository.commit()
        return user, []

    def _validate_registration(self, form_data):
        role = (form_data.get("role") or "").strip()
        if role not in self.VALID_ROLES:
            return ["Please choose a valid role before continuing."]

        required = ["full_name", "username", "email", "password", "confirm_password"]
        missing = [field for field in required if not (form_data.get(field) or "").strip()]
        if missing:
            return ["Please complete all required account fields."]

        if form_data["password"] != form_data["confirm_password"]:
            return ["Password confirmation does not match."]

        if len(form_data["password"]) < 6:
            return ["Password must be at least 6 characters long."]

        if role == "patient":
            patient_required = ["national_id", "phone"]
            if any(not (form_data.get(field) or "").strip() for field in patient_required):
                return ["Please complete all patient registration fields."]

        if role == "doctor":
            doctor_required = ["department_id", "title", "room_number", "employee_code"]
            doctor_values = {
                "department_id": form_data.get("department_id"),
                "title": form_data.get("title"),
                "room_number": form_data.get("room_number"),
                "employee_code": self._employee_code(form_data, role),
            }
            if any(not (doctor_values[field] or "").strip() for field in doctor_required):
                return ["Please complete all doctor registration fields."]
            if not self.repository.get_department(int(form_data["department_id"])):
                return ["The selected department could not be found."]

        if role == "secretary":
            if not self._employee_code(form_data, role) or not (form_data.get("phone") or "").strip():
                return ["Please complete all secretary registration fields."]

        return []

    def _employee_code(self, form_data, role):
        if role == "doctor":
            return (form_data.get("employee_code_doctor") or "").strip() or None
        if role == "secretary":
            return (form_data.get("employee_code_secretary") or "").strip() or None
        return None
