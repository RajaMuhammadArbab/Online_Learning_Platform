from django.contrib import admin
from .models import Course, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id","title","created_by","is_published","price","created_at")
    search_fields = ("title","created_by__username")
    list_filter = ("is_published",)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id","title","course","order","duration_seconds")
    search_fields = ("title","course__title")
