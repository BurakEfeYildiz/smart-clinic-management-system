from functools import wraps

from flask import flash, redirect, session, url_for

from clinic.repositories import ClinicRepository


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return ClinicRepository().get_user(user_id)


def require_role(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user:
                flash("Please choose a clinic role to continue.", "warning")
                return redirect(url_for("auth.login"))
            if roles and user.role not in roles:
                flash("This panel is not available for your current role.", "error")
                return redirect(url_for("dashboard.index"))
            return view_func(*args, **kwargs)

        return wrapper

    return decorator
