from flask import Blueprint, render_template

from clinic.controllers.helpers import current_user, require_role

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@require_role()
def index():
    user = current_user()
    template_by_role = {
        "secretary": "dashboard/secretary.html",
        "doctor": "dashboard/doctor.html",
        "patient": "dashboard/patient.html",
    }
    return render_template(template_by_role.get(user.role, "dashboard/secretary.html"), user=user)


@dashboard_bp.route("/not-implemented")
@require_role()
def not_implemented():
    return render_template("shared/not_implemented.html")
