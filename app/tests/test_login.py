from django.http import response
from django.test import TestCase
from django.urls import reverse
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
        login_data={
			"username":'testdata',
			'password':'Darshita@11'
		}
        response=self.client.post(reverse('login'),data=login_data)
        self.assertEqual(response.status_code, 200)

    def test_login_username(self):
        data={
            'username':'test',
            'password':'Darshita@11'
        }
        response=self.client.post(reverse('login'),data=data)
        self.assertNotEqual(response.status_code, 302)
      

    def test_login_password(self):
        data={
            'username':'testdata',
            'password':'dd'
        }
        response=self.client.post(reverse('login'),data=data)
        self.assertNotEqual(response.status_code, 302)
