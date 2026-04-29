from clinic.services.patient_flow_service import PatientFlowService


class FakeRepository:
    def __init__(self, flow_record):
        self.flow_record = flow_record
        self.committed = False

    def get_flow_record(self, flow_id):
        return self.flow_record

    def commit(self):
        self.committed = True


class FakeFlow:
    def __init__(self, status):
        self.current_status = status
        self.started_at = None
        self.completed_at = None
        self.appointment = None


def test_patient_flow_allows_waiting_to_in_exam():
    flow = FakeFlow("waiting")
    repository = FakeRepository(flow)
    service = PatientFlowService(repository)

    result, errors = service.update_status(1, "in_exam")

    assert errors == []
    assert result.current_status == "in_exam"
    assert result.started_at is not None
    assert repository.committed is True


def test_patient_flow_rejects_invalid_transition():
    flow = FakeFlow("completed")
    service = PatientFlowService(FakeRepository(flow))

    result, errors = service.update_status(1, "in_exam")

    assert result is None
    assert errors == ["This patient flow transition is not allowed."]
