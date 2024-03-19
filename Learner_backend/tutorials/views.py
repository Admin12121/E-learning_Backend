from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404
from .models import *
from .serializers import *
from users.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

class CourseDataView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        video_title = request.query_params.get('video_title')
        course_data = CourseData.objects.all()

        if video_title:
            course_data = course_data.filter(video_title=video_title)

        serializer = CourseDataSerializer(course_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SyllabusView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        syllabus_name = request.query_params.get('syllabus_name')
        syllabus = Syllabus.objects.all()

        if syllabus_name:
            syllabus = syllabus.filter(nameof_syllabus1=syllabus_name)

        serializer = SyllabusSerializer(syllabus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        course_name = request.query_params.get('name')  # Get the query parameter 'name'
        if course_name:
            courses = Courses.objects.filter(name=course_name)  # Filter courses by the provided name
        else:
            courses = Courses.objects.all()  # Retrieve all course instances if no name provided

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


