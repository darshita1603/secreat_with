from django.contrib.auth import get_user_model
from django.http import response
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class TestLogOutView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
			username='testdata', 
			password='Darshita@11',
            email="chavdadc88@gmail.com",
            first_name='darshita',
            last_name="chavda"
            )

    def test_login(self):
        data={
			"username":'testdata',
			'password':'Darshita@11'
		}
        login_response=self.client.post(reverse('login'),data=data)
        self.assertEqual(login_response.status_code, 200)

        token=login_response.data["token"]
        
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(login_response.status_code, 200)
