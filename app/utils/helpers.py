from flask import session, redirect

def login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return redirect("/auth/login")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
