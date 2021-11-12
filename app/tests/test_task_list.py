from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


class TestLoginView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testdata',
            password='Darshita@11',
            email="chavdadc88@gmail.com",
            first_name='darshita',
            last_name="chavda"
        )

    def test_login(self):
        data = {
            "username": 'testdata',
         			'password': 'Darshita@11'
        }
        login_response = self.client.post(reverse('login'), data=data)
        self.assertEqual(login_response.status_code, 200)

        token = login_response.data["token"]

        post_data = {
            "name_of_task": "abe",
            "details": "jj",
            "end_date": "2020-2-21",
            "end_time": "11:11:11"
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('tasklist'), data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(reverse('tasklist'))
