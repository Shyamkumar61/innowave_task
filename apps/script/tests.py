from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from apps.script.models import Script
from apps.account.models import Account
from apps.script.apis.serializers import ScriptSerializer
from rest_framework.test import APIClient

# Create your tests here.


class ScriptsModelTestCase(TestCase):

    def setUp(self):
        account = Account.objects.create(email="test@gmail", username="testuser", first_name='test', password='shyam')
        self.script = Script.objects.create(
            name='Test Script',
            category=Script.Smoke,
            owner=account,
            status=Script.Development
        )

    def test_script_model(self):
        script = Script.objects.get(name='Test Script')
        self.assertEqual(script.name, 'Test Script')
        self.assertEqual(script.category, Script.Smoke)
        self.assertEqual(script.owner.username, 'testuser')
        self.assertEqual(script.status, Script.Development)


class ScriptSerializerTestCase(TestCase):
    def test_valid_data(self):
        account = Account.objects.create(email="test@gmail", username="testuser", first_name='test', password='shyam')
        data = {
            'name': 'Test Script',
            'category': Script.Smoke,
            'owner': account.pk,
            'status': Script.Development
        }
        serializer = ScriptSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        account = Account.objects.create(email="test@gmail", username="testuser", first_name='test', password='shyam')
        data = {
            'name': '',
            'category': Script.Smoke,
            'owner': account.pk,
            'status': Script.Development
        }
        serializer = ScriptSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class ScriptViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        account = Account.objects.create(email="test1@gmail", username="testusers", first_name='test', password='shyam')
        self.script_data = {
            'name': 'Test Script',
            'category': Script.Smoke,
            'owner': account,
            'status': Script.Development
        }
        self.script = Script.objects.create(**self.script_data)
        self.url = reverse('scripts')

    def test_script_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_script(self):
        self.script_data['owner'] = Account.objects.get(username='testusers').id
        response = self.client.post(self.url, self.script_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_script_detail(self):
        detail_url = reverse('script-detail', kwargs={'pk': self.script.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.script_data['name'])

    def test_update_script(self):
        update_data = {
            'name': 'Updated Script',
            'category': Script.Performance,
            'owner': Account.objects.get(username='testusers').id,
            'status': Script.Completed
        }
        detail_url = reverse('script-detail', kwargs={'pk': self.script.pk})
        response = self.client.put(detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], update_data['name'])

    def test_delete_script(self):
        detail_url = reverse('script-detail', kwargs={'pk': self.script.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)