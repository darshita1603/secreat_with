from django.contrib.auth import get_user_model
from django.http import response
from django.test import TestCase


class RegisterView(TestCase):
    def setUp(self):
        self.user = get_user_model.objects.create_user(
            username='testdata',
            password='Darshita@11',
            password2='Darshita@11',
            email="chavdadc88@gmail.com",
            first_name='darshita',
            last_name="chavda"
        )
        self.assertRedirects(response, '/article/auth/login/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
