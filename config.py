
class Config:
    SECRET_KEY = "secret"
    LANGUAGES = ["ar", "fr", "en"]
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
