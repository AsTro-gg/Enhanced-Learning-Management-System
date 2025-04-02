from django.contrib import admin
from .models import Course, Enrollment, Assesment, Submission, Sponsorship, Notification,User

admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Assesment)
admin.site.register(Submission)
admin.site.register(Sponsorship)
admin.site.register(Notification)
admin.site.register(User)