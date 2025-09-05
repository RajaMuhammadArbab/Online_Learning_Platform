from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Enrollment, LessonProgress
from .serializers import EnrollmentSerializer, LessonProgressSerializer
from apps.courses.models import Course, Lesson


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related("student", "course").all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
       
        if hasattr(user, "is_admin") and user.is_admin():
            return Enrollment.objects.all()
        return Enrollment.objects.filter(student=user)

    @action(detail=True, methods=["post"])
    def enroll(self, request, pk=None):
        """
        POST /api/enrollments/{course_id}/enroll/
        Enroll the current logged-in student into a course.
        """
        course = get_object_or_404(Course, pk=pk)

        
        if hasattr(request.user, "is_student") and not request.user.is_student():
            return Response({"detail": "Only students can enroll"},
                            status=status.HTTP_403_FORBIDDEN)

        
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course
        )

        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def my_courses(self, request):
        qs = Enrollment.objects.filter(student=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def my_progress(self, request, pk=None):
        enrollment = get_object_or_404(Enrollment, pk=pk, student=request.user)
        return Response({
            "course_id": enrollment.course.id,
            "course_title": enrollment.course.title,
            "progress_percent": float(enrollment.progress),
        })

    @action(detail=True, methods=["post"], url_path="progress")
    def update_progress(self, request, pk=None):
       
        enrollment = get_object_or_404(Enrollment, pk=pk, student=request.user)
        progress = request.data.get("progress")

        if progress is None:
            return Response({"detail": "Progress value required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            progress = float(progress)
        except ValueError:
            return Response({"detail": "Progress must be a number"},
                            status=status.HTTP_400_BAD_REQUEST)

        enrollment.progress = max(0.0, min(100.0, progress))  # clamp 0–100
        enrollment.save()

        return Response({
            "message": "Progress updated",
            "course_id": enrollment.course.id,
            "course_title": enrollment.course.title,
            "progress_percent": float(enrollment.progress),
        })


class LessonProgressViewSet(viewsets.ModelViewSet):
    queryset = LessonProgress.objects.select_related("lesson", "enrollment").all()
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "is_admin") and user.is_admin():
            return LessonProgress.objects.all()
        return LessonProgress.objects.filter(enrollment__student=user)

    def create(self, request, *args, **kwargs):
        lesson_id = request.data.get("lesson_id")
        if not lesson_id:
            return Response({"detail": "lesson_id required"},
                            status=status.HTTP_400_BAD_REQUEST)

        lesson = get_object_or_404(Lesson, pk=lesson_id)
        enrollment = get_object_or_404(Enrollment, student=request.user, course=lesson.course)

        progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment, lesson=lesson
        )

        if not created:
            return Response({"detail": "Already marked as completed"},
                            status=status.HTTP_200_OK)

        serializer = LessonProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
