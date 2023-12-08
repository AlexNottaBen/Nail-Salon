#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import request

from targets.app import app


with app.test_request_context("/", method="GET"):
    assert request.path == "/"
    assert request.method == "GET"
    print("OK")
