from .views import *
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from.serializer import *
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import login as django_login,logout as django_logout
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        django_login(request,user)
        token,created=Token.objects.get_or_create(user=user)
        return Response({"message":"login Successfully","token":token.key},status=200)

@permission_classes([IsAuthenticated])
class LogOutView(APIView):
    def get(self,request):
        try:  
            request.user.auth_token.delete()
            django_logout(request)
            return Response({"message":"logout Successfully"},status=204)
        except request.user.auth_token.DoesNotExist:
             return HttpResponse({"message":"Please check token is not valid"},status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes=(TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self,queryset=None,):
        obj=self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        token=request.user.auth_token
        obj=self.request.user
        
        data={
            "token":token,
            "old_pwd":request.data.get("old_pwd"),
            "new_pwd":request.data.get("new_pwd")
        }
        
        serializer=ChangePasswordSerializer(data=data)
        if serializer.is_valid():
            if not obj.check_password(serializer.data.get("old_pwd")):
                return Response({"old_pwd":['Wrong password']},status=status.HTTP_400_BAD_REQUEST)
            else:
                obj.set_password(serializer.data.get("new_pwd"))
                obj.save()
                response={
                    'status':'success',
                    'code':status.HTTP_200_OK,
                    'message':'password update',
                    'data':[]
                }
                return Response(response)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',"POST"]) # not select basic auth 
@permission_classes([IsAuthenticated])
def task_list(request): 
    if request.method =='GET':
            token=request.user.auth_token
            dataa=Token.objects.filter(key=token).values_list("user_id",flat=True).first()
            user=Task.objects.filter(user__username=request.user)
            serializer=TaskSerializer(user,many=True)
            return Response(serializer.data)

    elif request.method=='POST':
        token=request.user.auth_token
        dataa=Token.objects.filter(key=token).values_list("user_id",flat=True).first()
       
        data={
            "user":request.user.id,
            "name_of_task":request.data['name_of_task'],
            "details":request.data['details'],
            "end_date":request.data['end_date'],
            "end_time":request.data['end_time']
        }
    
        serializer=TaskSerializer(data=data)

        if  serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

@permission_classes([IsAuthenticated])
@api_view(['GET','PUT','DELETE'])
def task_update(request,pk):
    try:
        task=Task.objects.get(pk=pk)

    except Task.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if request.method=='GET':
        serializer=TaskSerializer(task)
        return Response(serializer.data)

    elif request.method=="PUT":
        token=request.user.auth_token
        dataa=Token.objects.filter(key=token).values_list("user_id",flat=True).first()
        data={
            "user":request.user.id,
            "name_of_task":request.data['name_of_task'],
            "details":request.data['details'],
            "end_date":request.data['end_date'],
            "end_time":request.data['end_time']
        }
    
        serializer=TaskSerializer(task,data=data)
        if  serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

    elif request.method=="DELETE":
        token = request.user.auth_token
       
        userdata=Task.objects.get(pk=pk)
        exiting_token=userdata.user.auth_token

        if token ==exiting_token:
              task.delete()
              return Response({"message":"Delete Successfully"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'status_code':404,'message':'token invalid'})


        
