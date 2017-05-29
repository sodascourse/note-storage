from django.conf.urls import url, include

from auth_api.urls import urlpatterns as auth_api_urls
from simple_note.router import note_router

urlpatterns = [
    *auth_api_urls,
    url(r"^", include(note_router.urls, namespace="note-api")),
]
