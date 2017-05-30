import uuid

from django.conf import settings
from django.db import models


class NoteQuerySet(models.QuerySet):

    def owned_by(self, user):
        return self.filter(owner=user)


class Note(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    title = models.TextField(blank=True)
    content = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = NoteQuerySet.as_manager()

    class Meta:
        db_table = 'simple_note'
        index_together = (
            ('owner', 'updated_at'),
        )

    def __str__(self):
        return f'<Note: {self.title}>'
