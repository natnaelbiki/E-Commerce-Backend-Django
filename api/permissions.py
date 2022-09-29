from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		# Write permissions are only allowed to the author of a post
		return obj.author == request.user

class ReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
class IsAuthorized(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.data.user in obj.objects.all():
			return True