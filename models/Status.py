#! /usr/bin/python3
# -*- coding: utf-8 -*-

from app import database


class Status(database.Model):
    __tablename__ = "statuses"
    id = database.Column(database.Integer(), primary_key=True)
    status_name = database.Column(database.String(length=32), nullable=False)
