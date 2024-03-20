from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')

    user = authenticate(email=email, password=password)

    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
        try:
            User.objects.get(email=email)    # Checking if email exist
            return Response({'errors': {'non_field_errors': ["Password doesn't match"]}}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:            # Checking if User Input wrong password
            return Response({'errors': {'email': ["Email is not Valid"]}}, status=status.HTTP_404_NOT_FOUND) 
        
class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
  
  def perform_update(self, serializer):
        serializer.save()

  def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class UserInfoView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request, format=None):
        user_info_instance = request.user.userinfo
        if user_info_instance:
            serializer = UserInfoSerializer(user_info_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User info does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        userinfo_instance = request.user.userinfo
        serializer = UpdateUserInfoSerializer(userinfo_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User info updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     
class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

class ProjectView(APIView):
   renderer_classes = [UserRenderer]
   permission_classes = [IsAuthenticated]

   def post(self, request, format=None):
      serializer = ProjectsSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Project Created'}, status=status.HTTP_200_OK)
      else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
   def get(self, request, format=None):
       id = request.query_params.get('id')
       user = request.query_params.get('user')
       name = request.query_params.get('name')
       project_title = request.query_params.get('project_title')
       
       if name and project_title:
            projects = Projects.objects.filter(user__name=name, project_title=project_title)
       elif name:
            projects = Projects.objects.filter(user__name=name)
       elif id:
            projects = Projects.objects.filter(id=id)
       elif user:
            projects = Projects.objects.filter(user=user)
       elif project_title:
            projects = Projects.objects.filter(project_title=project_title)
       else:
            projects = Projects.objects.all()

       serializer = ProjectsSerializer(projects, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
 
   def patch(self,request,*args,**kwargs):
      id = request.query_params.get('id')
      name = request.query_params.get('name')
      project_title = request.query_params.get('project_title')

      if id and name and project_title:
        try:
          projects = Projects.objects.get(user__name=name,project_title=project_title,id=id)
          serializer = ProjectsSerializer(projects,data= request.data, partial= True)
          if serializer.is_valid():
             serializer.save()
             return Response({'msg': 'Project updated'}, status=status.HTTP_200_OK)
          return Response({'msg': 'invalid data'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'msg': 'invalid id or user'}, status=status.HTTP_403_FORBIDDEN)

   def delete(self, request, *args, **kwargs):
      id = request.query_params.get('id')
      name = request.query_params.get('name')
      
      if id and name :
        try:
          projects = Projects.objects.get(user__name=name, id=id)
          projects.delete()
          return Response({'msg': 'Project Deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': 'invalid id'}, status=status.HTTP_403_FORBIDDEN)
   

           