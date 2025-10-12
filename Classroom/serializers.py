# app/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from .models import Assignment, Submission, Announcement, Discussion,Reply

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        ) 
        return user


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'


class DiscussionSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Discussion
        fields = ['id', 'user', 'question', 'created_at', 'replies']