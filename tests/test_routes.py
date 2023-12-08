#! /usr/bin/python3
# -*- coding: utf-8 -*-

from requests import get
from unittest import TestCase, main


class RoutesTestCase(TestCase):
    def test_index_page(self):
        self.response = get("http://127.0.0.1:5000/")
        self.assertEqual(self.response.status_code, 200)

    def test_credits_page(self):
        self.response = get("http://127.0.0.1:5000/credits")
        self.assertEqual(self.response.status_code, 200)
        self.response = get("http://127.0.0.1:5000/credits/")
        self.assertEqual(self.response.status_code, 200)

    def test_login_page(self):
        self.response = get("http://127.0.0.1:5000/login")
        self.assertEqual(self.response.status_code, 200)
        self.response = get("http://127.0.0.1:5000/login/")
        self.assertEqual(self.response.status_code, 200)

    def test_signup_page(self):
        self.response = get("http://127.0.0.1:5000/signup")
        self.assertEqual(self.response.status_code, 200)
        self.response = get("http://127.0.0.1:5000/signup/")
        self.assertEqual(self.response.status_code, 200)

    def test_orders_page(self):
        self.response = get("http://127.0.0.1:5000/master/orders")
        self.assertEqual(self.response.status_code, 200)
        self.response = get("http://127.0.0.1:5000/master/orders/")
        self.assertEqual(self.response.status_code, 200)

    def test_logout(self):
        self.response = get("http://127.0.0.1:5000/logout")
        self.assertEqual(self.response.status_code, 200)
        self.response = get("http://127.0.0.1:5000/logout/")
        self.assertEqual(self.response.status_code, 200)

    def test_administrator_orders_page(self):
        self.response = get("http://127.0.0.1:5000/administrator/orders")
        self.assertEqual(self.response.status_code, 200)
        self.response = get("http://127.0.0.1:5000/administrator/orders/")
        self.assertEqual(self.response.status_code, 200)

    def test_create_page(self):
        self.response = get("http://127.0.0.1:5000/administrator/order/create")
        self.assertEqual(self.response.status_code, 200)
        self.response = get("http://127.0.0.1:5000/administrator/order/create/")
        self.assertEqual(self.response.status_code, 200)

    def test_users_page(self):
        self.response = get("http://127.0.0.1:5000/administrator/users")
        self.assertEqual(self.response.status_code, 200)
        self.response = get("http://127.0.0.1:5000/administrator/users/")
        self.assertEqual(self.response.status_code, 200)


if __name__ == "__main__":
    main()
