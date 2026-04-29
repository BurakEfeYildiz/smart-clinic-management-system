from flask import Blueprint, flash, redirect, render_template, request, url_for

from clinic.controllers.helpers import current_user, require_role
from clinic.repositories import ClinicRepository
from clinic.services import AvailabilityService

availability_bp = Blueprint("availability", __name__, url_prefix="/availability")


@availability_bp.route("/", methods=["GET", "POST"])
@require_role("doctor")
def index():
    user = current_user()
    doctor = user.doctor_profile
    service = AvailabilityService()

    if request.method == "POST":
        _, errors = service.create_availability(request.form, doctor.id)
        if errors:
            for error in errors:
                flash(error, "error")
        else:
            flash("Availability saved successfully.", "success")
            return redirect(url_for("availability.index"))

    items = ClinicRepository().list_doctor_availability(doctor_id=doctor.id)
    return render_template("availability/index.html", availability_items=items)
