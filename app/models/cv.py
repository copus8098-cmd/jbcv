from app import db
import uuid
import json

class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(36), unique=True, nullable=False)

    template = db.Column(db.String(50))
    language = db.Column(db.String(5))
    data = db.Column(db.Text)

    is_public = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
