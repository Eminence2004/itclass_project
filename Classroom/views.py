# classroom/views.py
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer
from .models import Announcement, Discussion, Reply
from .serializers import AnnouncementSerializer, DiscussionSerializer, ReplySerializer



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubmissionListCreateView(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]


# --- Announcements ---
class AnnouncementListCreateView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]


# --- Discussion Forum ---
class DiscussionListCreateView(generics.ListCreateAPIView):
    queryset = Discussion.objects.all().order_by('-created_at')
    serializer_class = DiscussionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReplyListCreateView(generics.ListCreateAPIView):
    queryset = Reply.objects.all().order_by('created_at')
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticated]