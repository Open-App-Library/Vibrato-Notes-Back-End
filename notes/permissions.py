from .models import Note, Notebook, Tag
from rest_framework import permissions


class CanViewOrEditNote(permissions.BasePermission):
    """
    Return True if the note belongs to the user
    or the user is doing a safe request to a public note.
    """
    message = "You do not have proper permissions for this note."

    def has_object_permission(self, request, view, note):
        user = request.user

        # If user is creator of note, return True
        if user == note.user:
            return True

        # If doing a safe operation and any of the conditions meet...
        # - note is public
        # - The note's notebook is public
        # ...return true!
        if request.method in permissions.SAFE_METHODS:
            if note.is_public or\
               (note.notebook and note.notebook.is_public):
                return True

        return False


class ValidateNoteNotebook(permissions.BasePermission):
    """
    If the user is creating or editing a note, ensure that
    the 'notebook' of the note is set to a valid notebook.
    """
    message = "Invalid notebook added to note."

    def has_permission(self, request, view):
        user = request.user

        if request.method in permissions.SAFE_METHODS or\
           request.method == "DELETE":
            return True

        notebookID = request.data.get('notebook', False)

        if not notebookID:
            return True  # User is not attempting to modify notebook

        notebook = Notebook.objects.filter(user=user,
                                           id=notebookID).first()

        if not notebook or notebook.user != user:
            return False  # Notebook is not valid

        return True


class ValidateNoteTags(permissions.BasePermission):
    """
    If the user is creating or editing a note, ensure that
    the 'tags' of the note are set to a valid tags.
    """
    message = "Invalid tag added to note."

    def has_permission(self, request, view):
        user = request.user

        if request.method in permissions.SAFE_METHODS or\
           request.method == "DELETE":
            return True

        # Go through tags in request. Return false if user
        # does not own tag or tag does not exist.
        for tagID in request.data.get('tags', []):
            tag = Tag.objects.filter(user=user,
                                     id=tagID).first()
            if not tag or tag.user != user:
                return False

        return True


class CanViewOrEditNotebook(permissions.BasePermission):
    """
    Return True if the notebook belongs to the user
    or the user is doing a safe request to a public notebook.
    """
    message = "You do not have permissions for this notebook."

    def has_object_permission(self, request, view, notebook):
        user = request.user

        # If user is creator of note, return True
        if user == notebook.user:
            return True

        # If doing a safe operation and any of the conditions meet...
        # - The notebook is public
        # ...return true!
        if request.method in permissions.SAFE_METHODS:
            if notebook.is_public:
                return True

        return False


class ValidateNotebookParent(permissions.BasePermission):
    """
    Return True is not creating or updating a notebook or if
    the request is not setting the parent or if
    the request is setting a valid parent.
    """
    message = "This notebook's parent is note valid."

    def has_permission(self, request, view):
        user = request.user

        if request.method in permissions.SAFE_METHODS or\
           request.method == 'DELETE':
            return True

        parentID = request.data.get('parent', None)
        if parentID is None:
            return True  # Notebook does not have parent

        parent = Notebook.objects.filter(user=user,
                                         parent__id=parentID).first()
        return parent  # If parent is exists, return True. Else, return False


class CanViewOrEditTag(permissions.BasePermission):
    """
    Return True if the tag is owned by the user
    """
    message = "You do not have proper permissions for this tag."

    def has_object_permission(self, request, view, tag):
        return request.user == tag.user
