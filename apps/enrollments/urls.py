from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet, LessonProgressViewSet

router = DefaultRouter()
router.register("enrollments", EnrollmentViewSet, basename="enrollments")
router.register("lesson-progress", LessonProgressViewSet, basename="lessonprogress")

urlpatterns = [
    path("", include(router.urls)),


    path(
        "courses/<int:course_pk>/enroll/",
        EnrollmentViewSet.as_view({"post": "create"}),
        name="course-enroll"
    ),
]
