from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView
from .views import AssignmentListCreateView, SubmissionListCreateView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list'),
    path('submissions/', SubmissionListCreateView.as_view(), name='submission-list'),
]