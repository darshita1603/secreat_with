from django.http import response
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from app.models import *
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
        self.name_of_task="bill",
        self.details="bill payment",
        self.end_date="2022-2-2",
        self.end_time="11:11:11",
    
    def test_login(self):
        data={
			"username":'testdata',
			'password':'Darshita@11'
		}
        login_response=self.client.post(reverse('login'),data=data)
        
        self.assertEqual(login_response.status_code, 200)

        token=login_response.data["token"]
       
        post_data={
            "name_of_task":self.name_of_task,
            "details":self.details,
            "end_date":self.end_date,
            "end_time":self.end_time
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('tasklist'),data=post_data)
    
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(reverse('tasklist'))
        task_data = list(Task.objects.all())

        for i in task_data:
            pk=i.pk
            

        response = client.put(f"/login/task-update/{pk}/", data=
            {   
                'name_of_task':'hii',
                'details':self.details,
                'end_date':self.end_date,
                'end_time':self.end_time,
            })
        self.assertEqual(response.status_code, 200)

        data_response = client.delete(f"/login/task-update/{pk}/")
        self.assertEqual(data_response.status_code, 204)

        users = Task.objects.all()
        self.assertEqual(users.count(), 0)
