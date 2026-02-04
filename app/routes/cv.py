from flask import Blueprint, render_template, render_template_string, request, send_file, redirect, url_for, session, abort
from app.services.pdf_export import generate_pdf
from app.models.cv import CV
from app import db
import uuid, json

cv_bp = Blueprint("cv", __name__)

# -----------------------
# Export PDF
# -----------------------
@cv_bp.route("/export-pdf", methods=["POST"])
def export_pdf():
    data = request.form
    template = data.get("template", "modern")
    language = data.get("language", "en")

    pdf_path = generate_pdf(template, data, language)

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="cv.pdf"
    )

# -----------------------
# Save CV (New)
# -----------------------
@cv_bp.route("/save", methods=["POST"])
def save_cv():
    form_data = request.form.to_dict(flat=False)
    user_id = session.get("user_id")
    is_public = request.form.get("is_public") == "on"

    cv = CV(
        slug=str(uuid.uuid4())[:8],
        template=form_data.get("template", ["modern"])[0],
        language=form_data.get("language", ["en"])[0],
        data=json.dumps(form_data, ensure_ascii=False),
        is_public=is_public,
        user_id=user_id
    )

    db.session.add(cv)
    db.session.commit()

    return redirect(url_for("cv.view_cv", slug=cv.slug))

# -----------------------
# View CV (Public / Private)
# -----------------------
@cv_bp.route("/view/<slug>")
def view_cv(slug):
    cv = CV.query.filter_by(slug=slug).first_or_404()

    # حماية Private CV
    if not cv.is_public and session.get("user_id") != cv.user_id:
        abort(403)

    data = json.loads(cv.data)

    return render_template(
        f"cv_templates/{cv.template}.html",
        data=data,
        lang=cv.language
    )

# -----------------------
# Toggle Public / Private
# -----------------------
@cv_bp.route("/toggle/<int:cv_id>")
def toggle_visibility(cv_id):
    user_id = session.get("user_id")
    cv = CV.query.get_or_404(cv_id)

    if cv.user_id != user_id:
        abort(403)

    cv.is_public = not cv.is_public
    db.session.commit()

    return redirect("/dashboard")

# -----------------------
# Delete CV
# -----------------------
@cv_bp.route("/delete/<int:cv_id>", methods=["POST"])
def delete_cv(cv_id):
    user_id = session.get("user_id")
    cv = CV.query.get_or_404(cv_id)

    if cv.user_id != user_id:
        abort(403)

    db.session.delete(cv)
    db.session.commit()
    return redirect("/dashboard")

# -----------------------
# Edit CV
# -----------------------
@cv_bp.route("/edit/<int:cv_id>", methods=["GET", "POST"])
def edit_cv(cv_id):
    user_id = session.get("user_id")
    cv = CV.query.get_or_404(cv_id)

    if cv.user_id != user_id:
        abort(403)

    if request.method == "POST":
        form_data = request.form.to_dict(flat=False)
        cv.template = form_data.get("template", [cv.template])[0]
        cv.language = form_data.get("language", [cv.language])[0]
        cv.is_public = request.form.get("is_public") == "on"
        cv.data = json.dumps(form_data, ensure_ascii=False)
        db.session.commit()
        return redirect("/dashboard")

    # GET → عرض الفورم مع البيانات الحالية
    data = json.loads(cv.data)
    return render_template("create_cv.html", data=data, editing=True, cv_id=cv.id)

# -----------------------
# Test CV Page (Dummy Data)
# -----------------------
@cv_bp.route("/view/test")
def view_test_cv():
    data = {
        "name": "Karim Salhif",
        "title": "Fullstack Developer",
        "education": [
            {"degree": "BSc Computer Science", "year": "2026", "school": "University X"}
        ],
        "experience": [
            {"company": "My Company", "role": "Developer", "year": "2025-2026"}
        ],
        "projects": [
            {"title": "CV Builder", "description": "Flask Project Example"}
        ]
    }
    return render_template("cv_templates/modern.html", data=data, lang="en")

# -----------------------
# Test Route Simple
# -----------------------
@cv_bp.route("/test")
def test_cv_page():
    return render_template_string("<h1>CV Test Page Works!</h1>")


@cv_bp.route("/create", methods=["GET"])
def create_cv():
    return render_template("create_cv.html", data={}, editing=False)
