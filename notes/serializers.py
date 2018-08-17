from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, Notebook, Tag

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
		user = User(
			email = validated_data['email'],
			first_name = validated_data['first_name'],
			last_name = validated_data['last_name'],
		)
		user.set_password(validated_data['password'])
		user.save()
		return user

class NotebookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notebook
		fields = ('id', 'title', 'parent', 'shared_with')

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ('id', 'title')

class NoteSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source="user.username")
	class Meta:
		model = Note
		fields = ('id', 'date_created', 'date_modified', 'title', 'text', 'notebook', 'tags', 'user', 'shared_with')

