from rest_framework.serializers import ModelSerializer

from simple_note.models import Note


class NoteSerializer(ModelSerializer):

    class Meta:
        model = Note
        exclude = 'id', 'owner', 'created_at', 'updated_at'

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs = self._add_owner(attrs)
        return attrs

    def _add_owner(self, attrs):
        request = self.context.get("request")
        if request:
            attrs["owner"] = request.user
        return attrs
