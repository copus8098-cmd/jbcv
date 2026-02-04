from flask import Blueprint, render_template, session, redirect
from app.models.cv import CV

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def index():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/auth/login")

    cvs = CV.query.filter_by(user_id=user_id).all()
    return render_template("dashboard/index.html", cvs=cvs)
