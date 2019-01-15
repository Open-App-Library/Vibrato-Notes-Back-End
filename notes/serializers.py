from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, Notebook, Tag
from django.db import IntegrityError


# For Profile Page
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


# For looking up other users
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',)


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ['email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = None
        try:
            user = User(email=validated_data['email'],
                        username=validated_data['email'],
                        first_name=validated_data['first_name'],
                        last_name=validated_data['last_name'])
            user.set_password(validated_data['password'])
            user.save()
        except IntegrityError as e:
            raise serializers.ValidationError(". ".join(e.args))
        return user


class NotebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notebook
        fields = ('sync_hash', 'id', 'title', 'parent', 'shared_with', 'row')
        read_only_fields = ('sync_hash',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('sync_hash', 'id', 'title')
        read_only_fields = ('sync_hash',)


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Note
        fields = ('sync_hash', 'id', 'date_created', 'date_modified', 'title', 'text',
                  'notebook', 'tags', 'user', 'shared_with', 'trashed',
                  'favorited')
        read_only_fields = ('sync_hash',)
