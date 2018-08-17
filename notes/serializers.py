from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, Notebook, Tag

# For Profile Page
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		ordering = ['-id']
		fields = ('id', 'first_name', 'last_name', 'username')

# For looking up other users
class PublicUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		ordering = ['-id']
		fields = ('first_name', 'last_name', 'username',)

class NotebookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notebook
		ordering = ['-id']
		fields = ('id', 'title', 'parent', 'shared_with')

class TagSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source="user.username")
	class Meta:
		model = Note
		ordering = ['-id']
		fields = ('id', 'title', 'text', 'notebook', 'tags', 'user', 'shared_with')

class NoteSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source="user.username")
	class Meta:
		model = Note
		ordering = ['-id']
		fields = ('id', 'title', 'text', 'notebook', 'tags', 'user', 'shared_with')

