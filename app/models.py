from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from .signals import *
# from django.core.mail import send_mail s 


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

#     email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "darshitactridhyatech@gmail.com"
#         # to:
#         [reset_password_token.user.email]
#     )

class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name_of_task=models.CharField(max_length=255)
    details=models.TextField()
    create_date=models.DateField(auto_now_add=True)
    end_date=models.DateField()
    create_time=models.TimeField(auto_now_add=True)
    end_time=models.TimeField()
    complete=models.BooleanField(default=False,null=True)
   