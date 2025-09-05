from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Course, Lesson
from .serializers import CourseSerializer, CourseCreateSerializer, LessonSerializer
from .permissions import IsCourseOwnerOrAdmin
from apps.users.permissions import IsInstructorOrAdmin

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("create","update","partial_update"):
            return CourseCreateSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        if not (self.request.user.is_instructor() or self.request.user.is_admin()):
            return Response({"detail":"Only instructor or admin can create courses."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        if not (request.user.is_admin() or (request.user.is_instructor() and course.created_by == request.user)):
            return Response({"detail":"Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_admin():
            return Response({"detail":"Admin only"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().select_related("course")
    serializer_class = LessonSerializer

    def create(self, request, *args, **kwargs):
        course_id = kwargs.get("course_pk") or request.data.get("course")
        if not course_id:
            return Response({"detail":"Course id required."}, status=status.HTTP_400_BAD_REQUEST)
        course = get_object_or_404(Course, pk=course_id)
        if not (request.user.is_admin() or (request.user.is_instructor() and course.created_by == request.user)):
            return Response({"detail":"Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        lesson = self.get_object()
        course = lesson.course
        if not (request.user.is_admin() or (request.user.is_instructor() and course.created_by == request.user)):
            return Response({"detail":"Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        lesson = self.get_object()
        course = lesson.course
        if not (request.user.is_admin() or (request.user.is_instructor() and course.created_by == request.user)):
            return Response({"detail":"Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
