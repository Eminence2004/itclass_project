from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assignment, Submission, Announcement, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Announcement)
def notify_students_on_announcement(sender, instance, created, **kwargs):
    if created:
        students = User.objects.filter(role='student')
        for student in students:
            Notification.objects.create(
                user=student,
                message=f"New announcement posted: {instance.title}"
            )

@receiver(post_save, sender=Submission)
def notify_instructor_on_submission(sender, instance, created, **kwargs):
    if created:
        instructor = instance.assignment.created_by
        Notification.objects.create(
            user=instructor,
            message=f"{instance.student.username} submitted '{instance.assignment.title}'"
        )
