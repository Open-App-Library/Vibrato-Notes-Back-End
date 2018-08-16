from rest_framework import permissions

class IsOwner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		user = request.user
		try:
			IsSharedWith = obj.shared_with.get(username=user.username)
		except:
			IsSharedWith = False
		# If the note was created by you, or shared with you -> TRUE
		if obj.user == user or IsSharedWith:
			return True
		return False

