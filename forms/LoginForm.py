#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import PasswordField, SubmitField, EmailField


class LoginForm(FlaskForm):
    email_address: EmailField = EmailField(
        label="Email", validators=[DataRequired()]
    )
    password: PasswordField = PasswordField(
        label="Password", validators=[DataRequired()]
    )
    submit: SubmitField = SubmitField(
        label="Log in"
    )
