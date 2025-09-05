from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id","title","description","video","order","duration_seconds")

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Course
        fields = ("id","title","slug","description","created_by","is_published","price","created_at","updated_at","lessons")

class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("title","description","is_published","price")
