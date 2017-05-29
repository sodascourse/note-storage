from http import HTTPStatus

from django.conf.urls import url, include
from django.http import JsonResponse

from auth_api.urls import urlpatterns as auth_api_urls
from simple_note.router import note_router


def handler404(request):
    resp = JsonResponse({"path": request.path, "message": "Not found."})
    resp.status_code = HTTPStatus.NOT_FOUND
    return resp


urlpatterns = [
    *auth_api_urls,
    url(r"^", include(note_router.urls, namespace="note-api")),
]
