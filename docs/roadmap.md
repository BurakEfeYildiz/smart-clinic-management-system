# Roadmap

## Phase 1 - Course Prototype

- Build layered MVC-style Flask structure.
- Use PostgreSQL as the main database.
- Provide role-based panels for secretary, doctor, and patient.
- Implement doctor availability management.
- Implement appointment creation with conflict prevention.
- Implement patient check-in and flow status transitions.
- Show complete UI navigation, including future modules.
- Show a clear not-implemented message for unfinished modules.

## Phase 2 - Hospital-Ready Expansion

- Replace demo role selection with secure authentication.
- Add prescription writing linked to medical records.
- Add patient history and clinical notes.
- Add lab result management.
- Add billing, invoices, and insurance workflows.
- Add admin screens for department, doctor, room, and role management.
- Add audit logs for clinical and scheduling actions.

## Phase 3 - Quality and Deployment

- Add integration tests with a test PostgreSQL database.
- Add CI checks.
- Add containerized deployment with Docker.
- Add user permissions and session hardening.
- Add reporting dashboards for clinic managers.
