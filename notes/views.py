from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .permissions import IsOwner, CanViewOrEditNoteOrNotebook
from .models import Note, Notebook, Tag
from .serializers import UserSerializer, UserCreationSerializer, PublicUserSerializer
from .serializers import NoteSerializer, NotebookSerializer, TagSerializer


def api_root(request, format=None):
    return JsonResponse({
        "message": "Welcome to the Vibrato API! Documentation coming soon."
    })


def oauth_code(request):
    return render(request, "oauth-code.html")


# User Views
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Allows logged-in user to view and change their profile details
class UserProfile(APIView):
    def get(self, request, format=None):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def put(self, request, format=None):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = get_object_or_404(User, pk=request.user.pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Allows you to view the bare-minimal info of other users - no personal info
class UserInfo(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "username"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# NOTE VIEWS ##
class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated, CanViewOrEditNoteOrNotebook,)
    queryset = Note.objects.all()
    ordering_fields = ('-id',)

    def get_queryset(self, *args, **kwargs):
        loggedin_user = self.request.user
        query = Note.objects.order_by('-id')
        query = query.filter(Q(user=loggedin_user) | Q(shared_with__in=[loggedin_user]))

        notebook = self.request.query_params.get("notebook", None)
        if notebook:
            query = query.filter(notebook__pk=notebook)

        tag = self.request.query_params.get("tag", None)
        if tag:
            tag_array = [x.strip() for x in tag.split(',')]
            query = query.filter(tags__in=tag_array)

        tag_force = self.request.query_params.get("!tag", None)
        if tag_force:
            tag_array = [x.strip() for x in tag_force.split(',')]
            for t in tag_array:
                query = query.filter(tags__in=[t])

        return query

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotebookViewSet(viewsets.ModelViewSet):
    serializer_class = NotebookSerializer
    permission_classes = (permissions.IsAuthenticated,
                          CanViewOrEditNoteOrNotebook,)
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
