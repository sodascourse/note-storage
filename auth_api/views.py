from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import CreateAPIView

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    error_message = "'{value}' is a registered {field}. Contact admin if you forgets password."

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            error_message = self.error_message.format(value=username, field="username")
            raise serializers.ValidationError(error_message)
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            error_message = self.error_message.format(value=email, field="email")
            raise serializers.ValidationError(error_message)
        return email

    def create(self, validated_data):
        data = validated_data.copy()
        password = data.pop("password")
        user = User(**data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        raise RuntimeError("Update is disallowed.")


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer
    authentication_classes = ()
