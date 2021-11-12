from django.db import router
from django.urls import path
from django.urls.conf import include
from django.urls.resolvers import URLPattern
from .views import LogOutView, LoginView,RegisterView,ChangePasswordView,task_list,task_update
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'register',RegisterView)

urlpatterns=[
    path('article/auth/login/',LoginView.as_view(),name="login"),
    path('logout/',LogOutView.as_view()),
    path('register/', RegisterView.as_view(), name='auth_register'),
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # path('api/password_reset/', SendFormEmail.as_view()),
    # path(r'^api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('task-list/',task_list,name="tasklist"),
    path('task-update/<int:pk>/',task_update,name="taskupdate"),
    path('task-update/',task_update,name="taskupdate"),

]