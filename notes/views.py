from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .permissions import IsOwner, NotePermissions, NotebookPermissions
from .models import Note, Notebook, Tag
from .serializers import NoteSerializer, NotebookSerializer, TagSerializer


def api_root(request, format=None):
    return JsonResponse({
        'documentation': request.build_absolute_uri('/docs/')
    })


def oauth_code(request):
    return render(request, "oauth-code.html")


# NOTE VIEWS ##
class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated,
                          NotePermissions,)
    queryset = Note.objects.all()
    ordering = "-date_modified"
    ordering_fields = ('id', 'date_created', 'date_modified', 'title',
                       'favorited')
    filter_fields = ('notebook',)

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return user.notes.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotebookViewSet(viewsets.ModelViewSet):
    serializer_class = NotebookSerializer
    permission_classes = (permissions.IsAuthenticated,
                          NotebookPermissions,)
    queryset = Notebook.objects.all()

    def get_queryset(self, *args, **kwargs):
        loggedin_user = self.request.user
        query = Notebook.objects.order_by('-id')
        query = query.filter(Q(user=loggedin_user) |
                             Q(shared_with__in=[loggedin_user]))
        return query

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Tag.objects.all()

    def get_queryset(self, *args, **kwargs):
        query = Tag.objects.order_by('-id')
        query = query.filter(user=self.request.user)
        return query

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
