from flask import Blueprint, render_template, render_template_string

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    # إذا لديك ملف home.html جاهز في templates
    try:
        return render_template("home.html")
    except:
        # مؤقتًا لتجربة الـ Route إذا لم يوجد home.html
        return render_template_string("""
            <h1>Home Page Works!</h1>
            <p><a href="/cv/view/test">View Test CV</a></p>
        """)
