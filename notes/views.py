from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions
from .permissions import IsOwner
from .models import Note
from .serializers import NoteSerializer, UserSerializer

# Views

## USER VIEWS ##

class UserList(generics.ListAPIView):
	permission_classes = (permissions.IsAdminUser,)
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	permission_classes = (permissions.IsAdminUser,)
	queryset = User.objects.all()
	serializer_class = UserSerializer

## NOTE VIEWS ##

class NoteList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Note.objects.all()
	serializer_class = NoteSerializer

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def get_queryset(self, *args, **kwargs):
		return Note.objects.all().filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class NoteDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
	permission_classes = (IsOwner,)
	queryset = Note.objects.all()
	serializer_class = NoteSerializer

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

