from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    CurrentUserView,
    AssignmentListCreateView,
    SubmissionListCreateView,
    GradeSubmissionView,
    ReplyListCreateView,
    AnnouncementViewSet,
    DiscussionViewSet
)

# -------------------- Router for ViewSets --------------------
router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'discussions', DiscussionViewSet, basename='discussion')

# -------------------- URL Patterns --------------------
urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Current user info
    path('me/', CurrentUserView.as_view(), name='current_user'),

    # Assignments & Submissions
    path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list'),
    path('submissions/', SubmissionListCreateView.as_view(), name='submission-list'),
    path('submissions/<int:pk>/grade/', GradeSubmissionView.as_view(), name='grade-submission'),

    # Replies (standalone listing)
    path('replies/', ReplyListCreateView.as_view(), name='reply-list'),

    # Announcements & Discussions via router
    path('', include(router.urls)),
]
