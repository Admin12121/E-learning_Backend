# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404
from .models import Courses, Syllabus, CourseData
from .serializers import CourseSerializer, SyllabusSerializer,CourseDataSerializer

class CourseDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CourseData.objects.all()
    serializer_class = CourseDataSerializer

class SyllabusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer

    @action(detail=True, methods=['GET'])
    def get_syllabus_entry(self, request, course_id=None, pk=None):
        if pk:
            syllabus_entry = self.get_object()
        elif course_id:
            course = Courses.objects.get(id=course_id)
            try:
                syllabus_entry = course.syllabi.get(id=pk)
            except Syllabus.DoesNotExist:
                raise Http404("Syllabus does not exist")
        else:
            raise Http404("Invalid request")

        serializer = SyllabusSerializer(syllabus_entry, context={'request': request})
        return Response(serializer.data)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all().order_by('name')
    serializer_class = CourseSerializer
    
    @action(detail=True, methods=['GET'])
    def get_syllabus_data(self, request, pk=None):
        course = self.get_object()
        
        syllabus_instances = course.syllabi.all()  # Retrieve all syllabus instances for the course
        serializer = SyllabusSerializer(syllabus_instances, many=True, context={'request': request})
        return Response(serializer.data)
