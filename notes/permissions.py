from rest_framework import permissions

class IsOwner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		user = request.user
		if obj.user == user:
			return True
		return False

class CanViewOrEditNoteOrNotebook(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		user = request.user
		# If the Notebook or Note is public
		if obj.notebook:
			if obj.notebook.is_public and request.method in permissions.SAFE_METHODS:
				return True
		if obj.is_public and request.method in permissions.SAFE_METHODS:
			return True
		try:
			IsSharedWith = obj.shared_with.get(username=user.username)
		except:
			IsSharedWith = False

		if not obj.user == user and request.method == "DELETE":
			return False # Shared user is most likely trying to delete note

		# If the note was created by you, or shared with you -> TRUE
		if obj.user == user or IsSharedWith:
			return True
		return False

