# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, SyllabusViewSet,CourseDataViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'syllabus', SyllabusViewSet, basename='syllabus')
router.register(r'coursedata', CourseDataViewSet, basename='coursedata')

urlpatterns = [
    path('courses/<int:course_id>/get_syllabus_data/<int:pk>/', SyllabusViewSet.as_view({'get': 'get_syllabus_entry'}), name='syllabus-get-syllabus-entry'),
    path('', include(router.urls)),
]
