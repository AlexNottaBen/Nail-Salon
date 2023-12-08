#! /usr/bin/python3
# -*- coding: utf-8 -*-

from app import database, bcrypt
from flask_login import UserMixin


class User(database.Model, UserMixin):
    __tablename__ = "users"
    id = database.Column(database.Integer(), primary_key=True)
    email_address = database.Column(
        database.String(length=319), nullable=False, unique=True
    )
    password_hash = database.Column(database.String(length=256), nullable=False)
    full_name = database.Column(database.String(length=128), nullable=False)
    work_experience = database.Column(database.Integer(), nullable=False)
    is_administrator = database.Column(
        database.Boolean(), nullable=False, default=False
    )

    @property
    def password(self) -> str:
        return self.password

    @password.setter
    def password(self, txt_password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(txt_password).decode(
            "utf-8"
        )

    def check_password_correction(self, attempted_password: str) -> bool:
        return bcrypt.check_password_hash(
            self.password_hash,
            attempted_password
        )

    def __str__(self) -> str:
        return self.full_name
