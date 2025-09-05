from django.contrib import admin
from .models import Enrollment, LessonProgress

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id","student","course","enrolled_at","is_active","progress")
    search_fields = ("student__username","course__title")

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("id","enrollment","lesson","watched","watched_at")
    search_fields = ("enrollment__student__username","lesson__title")
