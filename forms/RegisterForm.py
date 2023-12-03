#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, Email, EqualTo
from wtforms import SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired, ValidationError


class RegisterForm(FlaskForm):

    def validate_email_address(self, email_address_to_check: str) -> None:
        email_address: str = User.query.filter_by(
            email_address=email_address_to_check.data
        ).first()
        if email_address:
            message: str = "Email address already exists! Please try a different email address!"
            flash(
                message,
                category="danger",
            )
            raise ValidationError(
                message
            )

    full_name: StringField = StringField(
        label="Full Name",
        validators=[Length(3, 128), DataRequired()]
    )
    email_address: EmailField = EmailField(
        label="Email",
        validators=[Email(), DataRequired()]
    )
    password: PasswordField = PasswordField(
        label="Password",
        validators=[Length(8, 64), DataRequired()]
    )
    confirm_password: PasswordField = PasswordField(
        label="Confirm",
        validators=[EqualTo("password"), DataRequired()]
    )
    work_experience: IntegerField = IntegerField(
        label="Experience",
        validators=[Length(1, 2), DataRequired()]
    )
    submit: SubmitField = SubmitField(label="Sign up")
