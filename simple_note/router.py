from rest_framework import routers

from simple_note.views import NoteViewSet

note_router = routers.SimpleRouter(trailing_slash=False)
note_router.register(r'notes', NoteViewSet)
