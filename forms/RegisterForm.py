#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import flash
from flask_wtf import FlaskForm
from wtforms.validators import Length, Email, EqualTo
from wtforms.validators import DataRequired, ValidationError
from wtforms import StringField, PasswordField, SubmitField, IntegerField


class RegisterForm(FlaskForm):

    def validate_email_address(self, email_address_to_check) -> None:
        email_address = User.query.filter_by(
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

    full_name = StringField(
        label="Full Name",
        validators=[Length(3, 128), DataRequired()]
    )
    email_address = StringField(
        label="Email",
        validators=[Email(), DataRequired()]
    )
    password = PasswordField(
        label="Password",
        validators=[Length(8, 64), DataRequired()]
    )
    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[EqualTo("password"), DataRequired()]
    )
    work_experience = IntegerField(
        label="Work experience (number of years)",
        validators=[Length(1, 2), DataRequired()]
    )
    submit = SubmitField(label="Sign up")
