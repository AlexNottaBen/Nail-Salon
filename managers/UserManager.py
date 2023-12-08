#! /usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List, Callable

from app import database
from models.User import User
from flask_login import login_user, logout_user, current_user
from flask import flash, redirect
from forms.RegisterForm import RegisterForm
from forms.LoginForm import LoginForm
from werkzeug.wrappers.response import Response


class UserManager:
    """
    This class is responsible for user registration
    and authorization through SQLAlchemy and flask_login.
    """

    @staticmethod
    def register_new_user(form: RegisterForm) -> None:
        try:
            user_to_create: User = User(
                full_name=form.full_name.data,
                email_address=form.email_address.data,
                password=form.password.data,
                work_experience=form.work_experience.data,
            )
            database.session.add(user_to_create)
            database.session.commit()
            login_user(user_to_create)  # Automaticaly login after register
            flash(f"Success! Hello, {user_to_create.full_name}!", category="success")
        except Exception as _exception:
            print(
                "[WARNING] Exception has occured while adding new user to database:",
                _exception,
            )

    @staticmethod
    def login_exsist_user(form: LoginForm) -> None:
        attempted_user = User.query.filter_by(
            email_address=form.email_address.data
        ).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            print(f"Success! Hello, {attempted_user}!")
            flash(f"Success! Hello, {attempted_user}!", category="success")
            return redirect("/")
        else:
            flash(
                "Username and password are not correct! Please try again!",
                category="danger",
            )

    @staticmethod
    def get_all_users() -> List[User]:
        return User.query.all()

    @staticmethod
    def get_user_by_id_or_404(id: int) -> User:
        return User.query.filter_by(id=id).first_or_404()

    @staticmethod
    def check_current_user_permissions() -> bool:
        """
        Return True if current user is administrator unless False
        """
        try:
            return current_user.is_administrator
        except Exception as _exception:
            print("[WARNING] Exception has occured while checking user permmsion: ", _exception)
            return False
