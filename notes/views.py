from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import exception_handler
from rest_framework import permissions
from rest_framework import viewsets

from .permissions import CanViewOrEditNote, ValidateNoteNotebook, \
                         ValidateNoteTags
from .permissions import CanViewOrEditNotebook, ValidateNotebookParent
from .permissions import CanViewOrEditTag

from .models import Note, Notebook, Tag
from .serializers import NoteSerializer, NotebookSerializer, TagSerializer


def api_root(request, format=None):
    return JsonResponse({
        'documentation': request.build_absolute_uri('docs/')
    })


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response


def oauth_code(request):
    return render(request, "oauth-code.html")


# NOTE VIEWS ##
class NoteViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Get a note from its sync_hash.

    list:
    List your notes.

    create:
    Create a new note.
    """

    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated,
                          CanViewOrEditNote,
                          ValidateNoteNotebook,
                          ValidateNoteTags)
    queryset = Note.objects.all()
    lookup_field = "sync_hash"
    ordering_fields = ('id', 'date_created', 'date_modified', 'title',
                       'favorited')
    filter_fields = ('notebook',)

    def get_queryset(self):
        user = self.request.user
        return user.notes.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotebookViewSet(viewsets.ModelViewSet):
    serializer_class = NotebookSerializer
    permission_classes = (permissions.IsAuthenticated,
                          CanViewOrEditNotebook,
                          ValidateNotebookParent)
    queryset = Notebook.objects.all()
    lookup_field = "sync_hash"
    filter_fields = ('sync_hash', 'id', 'parent',)

    def get_queryset(self):
        user = self.request.user
        return user.notebooks.filter(parent__exact=None)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,
                          CanViewOrEditTag)
    queryset = Tag.objects.all()
    lookup_field = "sync_hash"

    def get_queryset(self):
        user = self.request.user
        return user.tags.filter()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
