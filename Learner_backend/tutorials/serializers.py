from rest_framework import serializers
from .models import *


class CourseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseData
        fields = ['content', 'video_title', 'videourl', 'codeType', 'note1', 'code1', 'image1', 'note2', 'code2', 'image2', 'note3', 'code3', 'image3', 'note4', 'code4', 'image4', 'note5', 'code5', 'image5']

class SyllabusSerializer(serializers.ModelSerializer):
    coursedata_set = CourseDataSerializer(many=True, read_only=True)

    class Meta:
        model = Syllabus
        fields = ['nameof_syllabus1', 'coursedata_set']

class CourseSerializer(serializers.ModelSerializer):
    syllabi = SyllabusSerializer(many=True, read_only=True)

    class Meta:
        model = Courses
        fields = ['name', 'syllabi']
