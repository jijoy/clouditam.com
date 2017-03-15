from django.contrib.auth import get_user_model
from rest_framework import serializers


# Serializers define the API representation.
class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.firstname')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        required_fields = ('email', )

    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
