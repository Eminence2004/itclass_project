from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import only the base views first
from .views import (
    RegisterView,
    CurrentUserView,
    AssignmentListCreateView,
    SubmissionListCreateView,
    GradeSubmissionView,
    ReplyListCreateView,
    AnnouncementViewSet,
    DiscussionViewSet,
    GenerateVoiceCallToken,
    EndVoiceCall,
    NotificationListView,  # ✅ make sure this is now defined in views.py
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

    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notification-list'),

    # Announcements & Discussions
    path('', include(router.urls)),

    # Voice Call Endpoints
    path('voice-call/token/', GenerateVoiceCallToken.as_view(), name='voice-call-token'),
    path('voice-call/end/', EndVoiceCall.as_view(), name='end-voice-call'),
]
