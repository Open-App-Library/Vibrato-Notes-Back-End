from django.http import Http404
from rest_framework import generics, mixins

from .models import Note
from .serializers import NoteSerializer

# Views

class NoteList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
	queryset = Note.objects.all()
	serializer_class = NoteSerializer

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

class NoteDetail(
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
	queryset = Note.objects.all()
	serializer_class = NoteSerializer

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)
