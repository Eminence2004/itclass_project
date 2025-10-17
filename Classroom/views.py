from rest_framework import generics, permissions, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import datetime
from django.contrib.auth import get_user_model
import uuid

from .models import (
    User, Assignment, Submission, Announcement, Discussion, Reply, Notification, VoiceCall
)
from .serializers import (
    UserSerializer,
    AssignmentSerializer,
    SubmissionSerializer,
    AnnouncementSerializer,
    DiscussionSerializer,
    ReplySerializer,
    NotificationSerializer
)
from .permissions import IsInstructor


# -------------------- Current User --------------------
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "id": user.id,
        })


# -------------------- User Registration --------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


# -------------------- Assignment --------------------
class IsStudent(BasePermission):
    """Allow only students to submit assignments"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    parser_classes = [MultiPartParser, FormParser]  # ✅ enables file upload

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsInstructor()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(instructor=request.user)

        # 🔔 Notify all students
        if request.user.role == 'instructor':
            students = User.objects.filter(role='student')
            for student in students:
                Notification.objects.create(
                    user=student,
                    message=f"📚 New assignment posted: {serializer.data.get('title', 'Untitled')}"
                )

        return Response(
            {"success": "Assignment created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )


# -------------------- Submission --------------------
class SubmissionListCreateView(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"success": "Submission created successfully", "data": serializer.data})


class GradeSubmissionView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsInstructor]

    def patch(self, request, *args, **kwargs):
        submission = self.get_object()
        grade = request.data.get('grade')
        submission.grade = grade
        submission.save()

        # 🔔 Notify student
        Notification.objects.create(
            user=submission.student,
            message=f"Your submission for '{submission.assignment.title}' has been graded. Grade: {submission.grade}"
        )

        return Response({"success": "Grade updated successfully", "grade": submission.grade})


# -------------------- Announcement --------------------
class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsInstructor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        User = get_user_model()
        students = User.objects.filter(role='student')
        for student in students:
            Notification.objects.create(
                user=student,
                message=f"📢 New announcement: {serializer.data.get('title', 'Untitled')}"
            )

        return Response({"success": "Announcement created successfully", "data": serializer.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"success": "Announcement updated successfully", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": "Announcement deleted successfully"})


# -------------------- Discussion --------------------
class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all().order_by('-created_at')
    serializer_class = DiscussionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsInstructor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 🔔 Notify instructors
        User = get_user_model()
        instructors = User.objects.filter(role='instructor')
        for instructor in instructors:
            Notification.objects.create(
                user=instructor,
                message=f"💬 New discussion started by {request.user.username}: {serializer.data.get('question')[:50]}..."
            )

        return Response({"success": "Discussion created successfully", "data": serializer.data})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reply(self, request, pk=None):
        discussion = self.get_object()
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, discussion=discussion)
            return Response({"success": "Reply added successfully", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------- Replies --------------------
class ReplyListCreateView(generics.ListCreateAPIView):
    queryset = Reply.objects.all().order_by('created_at')
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]


# -------------------- Notifications --------------------
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications.all().order_by('-created_at')


# -------------------- Voice Calls --------------------
class GenerateVoiceCallToken(APIView):
    """Generate a unique token (channel name) for a new voice call."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        channel_name = f"call_{uuid.uuid4().hex[:10]}"
        call = VoiceCall.objects.create(channel_name=channel_name, created_by=request.user)
        return Response({
            "success": "Voice call token generated successfully.",
            "channel_name": channel_name,
            "created_by": request.user.username,
            "created_at": call.created_at
        })


class EndVoiceCall(APIView):
    """End an active voice call."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        channel_name = request.data.get("channel_name")
        try:
            call = VoiceCall.objects.get(channel_name=channel_name, created_by=request.user)
            call.is_active = False
            call.ended_at = datetime.utcnow()
            call.save()
            return Response({"success": f"Call '{channel_name}' ended successfully."})
        except VoiceCall.DoesNotExist:
            return Response({"error": "Call not found or unauthorized."}, status=404)
