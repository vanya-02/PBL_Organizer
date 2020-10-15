from flask import Blueprint, request, redirect, url_for
from api.model import User, db
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from datetime import datetime

main = Blueprint('main', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@main.route("/")
@main.route("/register", methods=["GET", "POST"])
def register_point():
    if current_user.is_authenticated:
        return redirect(url_for("main.registered_error"))

    if request.method == 'POST':
        data = request.get_json()
        user = User()
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.creation_date = datetime.now()
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
    return {"msg": "registration was successful"}


@main.route("/registered_error")
def registered_error():
    return {"msg": "sorry, you are already logged in"}


@main.route("/login", methods=["GET", "POST"])
def login_point():
    if current_user.is_authenticated:
        return redirect(url_for("main.user_point"))

    if request.method == "POST":
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            return {"msg": "such user doesnt exist"}
        elif not user.check_password(data["password"]) or user.email != data["email"]:
            return {"msg": "invalid email or password"}

        login_user(user)

    return {"msg": "you have logged in"}


@main.route("/logout")
@login_required
def logout_point():
    logout_user()
    return {"msg": "you have been logged out  "}


@main.route("/profile")
@login_required
def user_point():
    return {"msg": "user endpoint"}


@main.route("/login/error")
def not_logged():
    return {"msg": "sorry, you are not logged"}
