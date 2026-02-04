from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# إنشاء DB
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    from app.routes.main import main_bp
    from app.routes.cv import cv_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(cv_bp, url_prefix="/cv")

    with app.app_context():
        db.create_all()

    return app



