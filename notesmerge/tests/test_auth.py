from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class AuthTests(APITestCase):

  def test_register_account(self):
    # user-list name is automatically generated http://www.django-rest-framework.org/api-guide/routers/
    url = reverse('user-list')
    data ={"username": "tttuserttt",
                  "password": "tttpassttt",}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(User.objects.count(), 1)
    self.assertEqual(User.objects.get().username, 'tttuserttt')


#https://github.com/evonove/django-oauth-toolkit/blob/master/oauth2_provider/tests/test_token_view.py
#http://stackoverflow.com/questions/27641703/how-to-test-an-api-endpoint-with-django-rest-framework-using-django-oauth-toolki
