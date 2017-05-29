from rest_framework.filters import BaseFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from simple_note.models import Note
from simple_note.serializers import NoteSerializer


class IsOwnerFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.owned_by(request.user)


class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.order_by("-updated_at")
    lookup_field = 'uuid'

    permission_classes = IsAuthenticated,
    filter_backends = IsOwnerFilterBackend,
