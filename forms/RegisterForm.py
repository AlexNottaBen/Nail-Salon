#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, Email, EqualTo
from wtforms import SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired, ValidationError
from models.User import User

class RegisterForm(FlaskForm):

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
        validators=[DataRequired()]
    )
    submit: SubmitField = SubmitField(label="Sign up")
