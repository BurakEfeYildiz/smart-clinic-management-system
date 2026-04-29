# Test Cases

| ID | Use Case | Input | Expected Output |
|---|---|---|---|
| TC-01 | Create appointment | Patient identity, doctor, available date/time, reason | Appointment is created with `scheduled` status. |
| TC-02 | Prevent appointment conflict | Same doctor, same date, same time | System rejects the second appointment. |
| TC-03 | Reject unavailable slot | Doctor/date/time outside availability | System shows an availability error. |
| TC-04 | Check in patient | Scheduled appointment ID | Patient flow record is created with `waiting` status. |
| TC-05 | Start examination | Waiting flow record | Status changes from `waiting` to `in_exam`. |
| TC-06 | Complete examination | In-exam flow record | Status changes from `in_exam` to `completed`. |
| TC-07 | Unfinished module | Click Prescription, Billing, Reports, Lab Results | UI shows `This function has not been implemented yet`. |

## Code Snippet for Presentation

```python
if self.repository.find_appointment_slot(doctor_id, appointment_date, appointment_time):
    return None, ["This doctor already has an appointment at the selected time."]

if not self._slot_is_available(doctor_id, appointment_date, appointment_time):
    return None, ["The selected time is outside the doctor's available schedule."]
```
