from django.urls import path, include
from .views import *

urlpatterns = [
    path('coursedata/', CourseDataView.as_view(), name='coursedata'),
    path('syllabus/', SyllabusView.as_view(), name='syllabus'),
    path('course/', CourseView.as_view(), name='course'),
]

# With this setup, you can make GET requests to the CourseDataView endpoint with query parameters to filter the data based on the specified fields. For example:

# To get all courses with the name "React", you would make a GET request to /course/?name=React
# To get all syllabi with the name "React Setup", you would make a GET request to syllabus/?syllabus_name=React%20Setup
# To get all course data with the video title "Installation of React", you would make a GET request to /coursedata/?video_title=Installation%20of%20React.