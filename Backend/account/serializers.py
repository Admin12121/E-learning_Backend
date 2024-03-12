from rest_framework import serializers
from account.models import *
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name' , 'password', 'password2', 'tc']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs
  
  #Email validator
  def validate_email(self, value):
        """
        Validate that the email is not already in use.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value
   

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']


class CourseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetails
        fields = [ 'active_course','user']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Include the course name in the representation
        representation['active_course_name'] = instance.active_course.name if instance.active_course else None
        return representation

class UpdateUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['profile', 'bio', 'address']

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['user', 'profile', 'bio', 'address']

class ProjectsSerializer(serializers.ModelSerializer):
   class Meta:
      model = Projects
      fields = ['id','user','project_title','project_type','description','html_code','css_code','js_code']


class UserProfileSerializer(serializers.ModelSerializer):
    userinfo = UserInfoSerializer()
    courseinfo = CourseDetailsSerializer(many=True, read_only=True)
    projects = ProjectsSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'tc', 'userinfo', 'courseinfo', 'projects')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Retrieve and include CourseDetails data
        course_details = CourseDetails.objects.filter(user=instance)
        course_info_data = CourseDetailsSerializer(course_details, many=True).data
        data['courseinfo'] = course_info_data

        # Retrieve and include Projects data
        projects_data = Projects.objects.filter(user=instance)
        projects_data_serialized = ProjectsSerializer(projects_data, many=True).data
        data['projects'] = projects_data_serialized

        return data
    
    def create(self, validated_data):
        userinfo_data = validated_data.pop('userinfo', {})
        courseinfo_data = validated_data.pop('courseinfo', [])  # Handle courseinfo data as a list
        project_data = validated_data.pop('projects',[])
        user = User.objects.create(**validated_data)

        UserInfo.objects.create(user=user, **userinfo_data)

        # Create Course_Details instances for each course
        for course_data in courseinfo_data:
            CourseDetails.objects.create(user=user, **course_data)
        
        for project in project_data:
           Projects.objects.create(user=user, **project)

        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.tc = validated_data.get('tc', instance.tc)
        instance.save()

        userinfo_data = validated_data.get('userinfo', {})
        userinfo_instance = instance.userinfo
        if userinfo_instance:
            userinfo_instance.profile = userinfo_data.get('profile', userinfo_instance.profile)
            userinfo_instance.bio = userinfo_data.get('bio', userinfo_instance.bio)
            userinfo_instance.address = userinfo_data.get('address', userinfo_instance.address)
            userinfo_instance.save()

        # Update courseinfo fields
        courseinfo_data = validated_data.get('courseinfo', [])
        current_courses = CourseDetails.objects.filter(user=instance)

        # Iterate through the provided course data
        for course_data in courseinfo_data:
            course_id = course_data.get('active_course', None)

            if course_id:
                # Get or create Course_Details instance for the given course_id
                course_instance, _ = current_courses.get_or_create(active_course_id=course_id)
                # Update fields if necessary
                course_instance.save()

        return instance

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password ' + link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
  