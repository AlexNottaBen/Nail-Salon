#! /usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List

from werkzeug import Response

from app import database
from models.User import User
from flask_login import login_user, current_user
from flask import flash, redirect
from forms.RegisterForm import RegisterForm
from forms.LoginForm import LoginForm


class UserManager:
    """
    This class is responsible for user registration
    and authorization through SQLAlchemy and flask_login.
    """

    @staticmethod
    def register_new_user(form: RegisterForm) -> None:
        """
        Register a new user based on the provided registration form.

        Args:
            form (RegisterForm): The registration form containing user details.
        """
        try:
            user_to_create: User = User(
                full_name=form.full_name.data,
                email_address=form.email_address.data,
                password=form.password.data,
                work_experience=form.work_experience.data,
            )
            database.session.add(user_to_create)
            database.session.commit()
            login_user(user_to_create)  # Automatically login after register
            flash(f"Success! Hello, {user_to_create.full_name}!", category="success")
        except Exception as _exception:
            print(
                "[WARNING] Exception has occurred while adding new user to database:",
                _exception,
            )

    @staticmethod
    def login_exists_user(form: LoginForm) -> Response:
        """
        Log in an existing user based on the provided login form.

        Args:
            form (LoginForm): The login form containing user credentials.

        Returns:
            Response: A werkzeug Response object.
        """
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
        """
        Retrieve a list of all users in the system.

        Returns:
            List[User]: A list of User objects.
        """
        return User.query.all()

    @staticmethod
    def get_user_by_id_or_404(user_id: int) -> User:
        """
        Retrieve a user by their user_id or raise a 404 error if not found.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The User object.

        Raises:
            404NotFound: If the user with the given ID is not found.
        """
        return User.query.filter_by(id=user_id).first_or_404()

    @staticmethod
    def check_current_user_permissions() -> bool:
        """
        Return True if current user is administrator, unless/otherwise False
        """
        try:
            return current_user.is_administrator
        except Exception as _exception:
            print(
                "[WARNING] Exception has occurred while checking user permission: ",
                _exception,
            )
            return False
