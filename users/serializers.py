from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class UserProfileSerializerRead(serializers.ModelSerializer):
    """Сериалайзер профиля пользователя"""

    user_id = serializers.IntegerField(source='user__id', required=False)
    profile_id = serializers.IntegerField(source='id', required=False)
    username = serializers.CharField(source='user__username', required=False)
    email = serializers.EmailField(source='user__email', required=False)

    class Meta:
        model = Profile
        fields = ('profile_id', 'user_id', 'username', 'email', 'ref_code', 'ref_by')


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер профиля пользователя"""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    """Сериалайзер профиля пользователя"""

    class Meta:
        model = Profile
        fields = ('id', 'user', 'ref_code', 'expiration_date', 'ref_by')
