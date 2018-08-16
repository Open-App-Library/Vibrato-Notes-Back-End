from rest_framework import permissions

class IsOwner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		print("THE BOOLEAN:", obj.user, request.user)
		return obj.user == request.user

