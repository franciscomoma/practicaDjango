from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)

        user.set_password(validated_data.get('password'))
        user.save()

        return user

    def update(self, instance, validated_data):
        instance = super(UserSerializer, self).update(instance, validated_data)

        instance.set_password(validated_data.get('password'))
        instance.save()

        return instance

    def get_fields(self):
        fields = super(UserSerializer, self).get_fields()

        if 'view' in self.context and self.context['view'].action in ('list', 'retrieve', 'me'):
            fields.pop('password')

        return fields