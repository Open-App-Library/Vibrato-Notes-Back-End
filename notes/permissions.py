from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.user == user:
            return True
        return False


class NotePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, note):
        user = request.user

        # If user is creator of note, return True
        if user == note.user:
            return True

        # If doing a safe operation and any of the conditions meet...
        # - note is public
        # - user is shared this note
        # - The note's notebook is public
        # - The user is shared the note's notebook
        # ...return true!
        if request.method in permissions.SAFE_METHODS:
            if note.is_public or\
               user in note.shared_with.all() or\
               (note.notebook and note.notebook.is_public) or\
               (note.notebook and user in note.notebook.shared_with):
                return True

        return False


class NotebookPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, notebook):
        user = request.user

        # If user is creator of note, return True
        if user == notebook.user:
            return True

        # If doing a safe operation and any of the conditions meet...
        # - The notebook is public
        # - The user is shared the notebook
        # ...return true!
        if request.method in permissions.SAFE_METHODS:
            if notebook.is_public or\
               user in notebook.shared_with:
                return True

        return False
