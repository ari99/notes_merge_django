from .merger.merger import Merger
from .models.merge import Merge
from typing import Dict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from django.contrib.auth.models import User
from notesmerge.serializers import UserSerializer, MergeSerializer
from rest_framework import viewsets
from notesmerge.permissions import IsOwner, UsersPermissions
from rest_framework.views import APIView
from oauth2_provider.ext.rest_framework import IsAuthenticatedOrTokenHasScope


'''
 ViewSet to create, list and update Merges.
'''
class MergeViewSet(viewsets.ModelViewSet):
  #https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/permissions.html
  permission_classes = [IsOwner, IsAuthenticatedOrTokenHasScope,]
  required_scopes = ['read','write']
  serializer_class = MergeSerializer

  def get_queryset(self):
    if self.request.user.is_superuser:
      return Merge.objects.all()
    else:
      return self.request.user.merges.all()

  '''
    Save the Merge with its owner User
  '''
  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

'''
 ViewSet to create, list and update Users.
'''
class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (UsersPermissions,)
  required_scopes = ['read','write']


'''
  APIView to perform the merge logic and return the result.
'''
class DoMerge(APIView):

  def post(self, request: Request, format=None) -> Response:
    return Response(self.do_merge(request.data['inputs'], request.data['merge_options']), status=status.HTTP_200_OK)

  def do_merge(self, inputs: Dict, merge_options: Dict) -> Dict:
    merger = Merger(inputs, merge_options)
    result = merger.merge()
    return result
