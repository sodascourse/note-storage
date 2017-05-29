import base64
import json
import uuid
from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.response import Response

from simple_note.models import Note

pytestmark = pytest.mark.django_db

User = get_user_model()


def expected_note(note: Note) -> dict:
    return {
        "uuid": str(note.uuid),
        "title": note.title,
        "content": note.content,
    }


@pytest.fixture(autouse=True)
def db_setup():
    user_1, user_2 = _setup_user()
    Note.objects.bulk_create(
        Note(title=f"Untitled note {idx}", content=f"Note content {idx}", owner=user_1)
        for idx in range(10)
    )
    Note.objects.bulk_create(
        Note(title=f"Untitled note {idx}", content=f"Note content {idx}", owner=user_2)
        for idx in range(5)
    )


def _setup_user():
    user_1 = User.objects.create(username="user-1")
    user_1.set_password("user-1-pw")
    user_1.save()
    user_2 = User.objects.create(username="user-2")
    return user_1, user_2


def auth_header(username, password):
    payload = f"{username}:{password}"
    base64_bytes: bytes = base64.b64encode(payload.encode("utf-8"))
    base64_str = base64_bytes.decode("utf-8")
    return {
        "HTTP_AUTHORIZATION": f'Basic {base64_str}',
    }


def test_list_is_auth_required(client):
    resp: Response = client.get(reverse("note-api:note-list"))
    assert resp.status_code == HTTPStatus.UNAUTHORIZED


def test_list_user_1_notes(client):
    user_1 = User.objects.get(username="user-1")
    resp: Response = client.get(reverse("note-api:note-list"),
                                **auth_header(username="user-1", password="user-1-pw"))
    assert resp.status_code == HTTPStatus.OK
    assert resp["Content-Type"] == "application/json"
    assert resp.data == [expected_note(note) for note
                         in Note.objects.owned_by(user_1).order_by("-updated_at")]


def test_retrieve_is_auth_required(client):
    note = Note.objects.last()
    resp: Response = client.get(reverse("note-api:note-detail", kwargs={"uuid": str(note.uuid)}))
    assert resp.status_code == HTTPStatus.UNAUTHORIZED


def test_retrieve_user_1_note(client):
    user_1 = User.objects.get(username="user-1")
    note = Note.objects.owned_by(user_1).last()
    resp: Response = client.get(reverse("note-api:note-detail", kwargs={"uuid": str(note.uuid)}),
                                **auth_header(username="user-1", password="user-1-pw"))
    assert resp.status_code == HTTPStatus.OK
    assert resp["Content-Type"] == "application/json"
    assert resp.data == expected_note(note)


def test_retrieve_user_2_note_is_not_found(client):
    user_2 = User.objects.get(username="user-2")
    note = Note.objects.owned_by(user_2).last()
    resp: Response = client.get(reverse("note-api:note-detail", kwargs={"uuid": str(note.uuid)}),
                                **auth_header(username="user-1", password="user-1-pw"))
    assert resp.status_code == HTTPStatus.NOT_FOUND


def test_create_is_auth_required(client):
    resp: Response = client.post(reverse("note-api:note-list"))
    assert resp.status_code == HTTPStatus.UNAUTHORIZED


def test_create_note(client):
    data = {"title": "test-title", "content": "test-content"}
    resp: Response = client.post(reverse("note-api:note-list"),
                                 json.dumps(data), content_type="application/json",
                                 **auth_header(username="user-1", password="user-1-pw"))
    assert resp.status_code == HTTPStatus.CREATED
    assert resp["Content-Type"] == "application/json"
    created_note = Note.objects.get(uuid=uuid.UUID(resp.data["uuid"]))
    assert created_note.title == "test-title"
    assert created_note.content == "test-content"
    assert created_note.owner == User.objects.get(username="user-1")
