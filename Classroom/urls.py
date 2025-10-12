from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView
from .views import (
    AssignmentListCreateView, SubmissionListCreateView,
    AnnouncementListCreateView, DiscussionListCreateView, ReplyListCreateView
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list'),
    path('submissions/', SubmissionListCreateView.as_view(), name='submission-list'),
     path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list'),
    path('submissions/', SubmissionListCreateView.as_view(), name='submission-list'),
    path('announcements/', AnnouncementListCreateView.as_view(), name='announcement-list'),
    path('discussions/', DiscussionListCreateView.as_view(), name='discussion-list'),
    path('replies/', ReplyListCreateView.as_view(), name='reply-list'),
]