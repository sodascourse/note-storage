import json
from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.response import Response

pytestmark = pytest.mark.django_db

User = get_user_model()


def test_signup_creates_new_user(client):
    data = {"username": "test-account",
            "password": "test-password",
            "email": "test@sodas.tw"}
    resp: Response = client.post(reverse("signup"), json.dumps(data),
                                 content_type="application/json")
    assert resp.status_code == HTTPStatus.CREATED
    user = User.objects.get(username="test-account")
    assert user.username == "test-account"
    assert user.email == "test@sodas.tw"
    assert user.check_password("test-password")
    assert resp.data == {
        "username": "test-account",
        "email": "test@sodas.tw",
    }


def test_signup_requires_three_fields(client):
    resp: Response = client.post(reverse("signup"))
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert "username" in resp.data
    assert "password" in resp.data
    assert "email" in resp.data


def test_signup_denies_duplicated_username(client):
    User.objects.create(username="test-account")

    data = {"username": "test-account",
            "password": "test-password",
            "email": "test@sodas.tw"}
    resp: Response = client.post(reverse("signup"), json.dumps(data),
                                 content_type="application/json")
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert "username" in resp.data
    assert User.objects.filter(username="test-account").count() == 1


def test_signup_denies_duplicated_email(client):
    User.objects.create(username="test-account", email="test@sodas.tw")

    data = {"username": "test-account-2",
            "password": "test-password",
            "email": "test@sodas.tw"}
    resp: Response = client.post(reverse("signup"), json.dumps(data),
                                 content_type="application/json")
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert "email" in resp.data
    assert User.objects.filter(email="test@sodas.tw").count() == 1
