from rest_framework.serializers import ModelSerializer, DateTimeField

from simple_note.models import Note


class NoteSerializer(ModelSerializer):

    modified_time = DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Note
        exclude = 'id', 'owner', 'created_at', 'updated_at'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        view = self.context.get("view")
        if view and view.action == "list":
            self.fields.pop("content")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs = self._add_owner(attrs)
        return attrs

    def _add_owner(self, attrs):
        request = self.context.get("request")
        if request:
            attrs["owner"] = request.user
        return attrs
