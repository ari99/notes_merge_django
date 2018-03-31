from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from oauth2_provider.models import get_application_model, AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings

from django.contrib.auth.models import User
from ..models.merge import Merge
from ..models.merge_options import MergeOptions
from django.utils import timezone
import datetime

Application = get_application_model()



class MergeApiTests(APITestCase):
  def setUp(self):
    self.test_user = User.objects.create_user("test_user", "test@user.com", "123456")

    self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
    self.application.save()
    oauth2_settings._SCOPES = ['read', 'write']
    self.token = AccessToken.objects.create(
            user=self.test_user, token='1234567890',
            application=self.application, scope='read write',
            expires=timezone.now() + datetime.timedelta(days=1)
        ).token


  def tearDown(self):
    self.application.delete()
    self.test_user.delete()

  #python manage.py test notesmerge.tests.test_merge_api.MergeApiTests.test_merge_list
  def test_merge_list(self):
    merge = Merge.objects.create()
    merge.name = "test merge1"
    merge.owner = self.test_user

    merge.save()
    MergeOptions.objects.create(merge=merge)

    url = reverse('merges-list')
    self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
    response = self.client.get(url)
    self.assertEqual(1, len(response.data))
    self.assertEqual(response.data[0].get("name"), "test merge1")

  
  def test_merge_save(self):
    url = reverse('merges-list')
    data_str = '{"id":null,"name":"first merge","inputs":[{"text":"ab1"},{"text":"ab2"}],"result":"ab1","merge_options":{"porter_stemmer":false,"remove_stop_words":false,"alphanumeric_filter":false,"output_delimiter":"\\n\\n","numeric_filter":false,"lowercase":false,"input_delimiter":"\\n\\n","wordnet_lemmatizer":false,"alpha_filter":true},"input_counter":4}'
    self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
    response = self.client.post(url, data_str, content_type='application/json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Merge.objects.count(), 1)
    self.assertEqual(Merge.objects.get().name, 'first merge')


  def test_merge_update(self):
    merge = Merge.objects.create()
    merge.name = "test merge1"
    merge.owner = self.test_user
    merge.save()
    MergeOptions.objects.create(merge=merge)

    url = reverse('merges-detail', args=[str(merge.id)])
    data_str = '{"id":null,"name":"updated","inputs":[{"text":"ab1"},{"text":"ab2"}],"result":"ab1","merge_options":{"porter_stemmer":false,"remove_stop_words":false,"alphanumeric_filter":false,"output_delimiter":"\\n\\n","numeric_filter":false,"lowercase":false,"input_delimiter":"\\n\\n","wordnet_lemmatizer":false,"alpha_filter":true},"input_counter":4}'
    self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
    response = self.client.put(url, data_str, content_type='application/json')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(Merge.objects.count(), 1)
    self.assertEqual(Merge.objects.get().name, 'updated')


