from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from clinic.repositories import ClinicRepository
from clinic.services import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return render_template("public/home.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user, errors = AuthService().login(
            request.form.get("username"),
            request.form.get("password"),
        )
        if errors:
            for error in errors:
                flash(error, "error")
        else:
            session["user_id"] = user.id
            return redirect(url_for("dashboard.index"))

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    repository = ClinicRepository()
    departments = repository.list_departments()

    if request.method == "POST":
        user, errors = AuthService(repository).register(request.form)
        if errors:
            for error in errors:
                flash(error, "error")
        else:
            session["user_id"] = user.id
            flash("Your account has been created successfully.", "success")
            return redirect(url_for("dashboard.index"))

    return render_template("auth/register.html", departments=departments)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
