from rest_framework import permissions
from oauth2_provider.ext.rest_framework import IsAuthenticatedOrTokenHasScope

'''
Custom permission to only allow owners of an object to edit it.
'''
class IsOwnerOrReadOnly(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):
    # Read permissions are allowed to any request,
    # so we'll always allow GET, HEAD or OPTIONS requests.
    if request.method in permissions.SAFE_METHODS:
      return True

    # Write permissions are only allowed to the owner of the snippet.
    return obj.owner == request.user


'''
Custom permission to only allow owners of an object to edit or read it.
'''
class IsOwner(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user and request.user.is_authenticated()

  def has_object_permission(self, request, view, obj):
    return obj.owner == request.user

#https://github.com/tomchristie/django-rest-framework/issues/1067
'''
  Allow anyone to register a user and Admin to list all users
'''
class UsersPermissions(permissions.BasePermission):
  def has_permission(self, request, view):
    isAdminUserPermission = permissions.IsAdminUser()
    if view.action == 'create':
      return True
    if view.action == 'list':
      return permissions.IsAdminUser().has_permission(request, view)
    else:
      return permissions.IsAdminUser().has_permission(request, view) or \
                   (IsAuthenticatedOrTokenHasScope().has_permission(request, view)
                            and permissions.DjangoModelPermissions().has_permission(request, view))

