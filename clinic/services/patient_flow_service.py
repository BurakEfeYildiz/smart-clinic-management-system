from datetime import datetime

from clinic.repositories import ClinicRepository


class PatientFlowService:
    ALLOWED_TRANSITIONS = {
        "waiting": {"in_exam", "cancelled"},
        "in_exam": {"completed"},
        "completed": set(),
        "cancelled": set(),
    }

    def __init__(self, repository=None):
        self.repository = repository or ClinicRepository()

    def update_status(self, flow_id, next_status):
        flow_record = self.repository.get_flow_record(flow_id)
        if not flow_record:
            return None, ["Patient flow record could not be found."]

        allowed = self.ALLOWED_TRANSITIONS.get(flow_record.current_status, set())
        if next_status not in allowed:
            return None, ["This patient flow transition is not allowed."]

        flow_record.current_status = next_status
        if next_status == "in_exam":
            flow_record.started_at = datetime.utcnow()
            if flow_record.appointment:
                flow_record.appointment.status = "in_exam"
        if next_status == "completed":
            flow_record.completed_at = datetime.utcnow()
            if flow_record.appointment:
                flow_record.appointment.status = "completed"

        self.repository.commit()
        return flow_record, []
