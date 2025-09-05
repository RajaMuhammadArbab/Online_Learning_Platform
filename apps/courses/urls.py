from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet

router = DefaultRouter()
router.register("courses", CourseViewSet, basename="courses")   # /api/courses/
router.register("lessons", LessonViewSet, basename="lessons")   # /api/lessons/

urlpatterns = [
    path("", include(router.urls)),
]
