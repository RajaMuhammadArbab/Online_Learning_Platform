from rest_framework import serializers
from .models import Enrollment, LessonProgress
from apps.courses.serializers import CourseSerializer
from apps.courses.models import Course   


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source="course", queryset=Course.objects.all()  
    )
    student = serializers.ReadOnlyField(source="student.username")

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "student",
            "course",
            "course_id",
            "enrolled_at",
            "is_active",
            "progress",
        )
        read_only_fields = (
            "id",
            "student",
            "course",
            "enrolled_at",
            "is_active",
            "progress",
        )


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ("id", "enrollment", "lesson", "watched", "watched_at")
        read_only_fields = ("watched_at",)

