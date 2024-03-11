from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.views import *
from rest_framework_simplejwt.views import(
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'activecourse', CourseDetailsViewSet, basename="activecourse")
router.register(r'project', ProjectViewSet, basename="project")

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('userinfo/', UserInfoView.as_view(), name='update-userinfo'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
    

]