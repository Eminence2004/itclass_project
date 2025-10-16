from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Classroom, Assignment, Submission

# Register your models here.
User = get_user_model()

# Register your models
admin.site.register(User)
admin.site.register(Classroom)
admin.site.register(Assignment)
admin.site.register(Submission)



