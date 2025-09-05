from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("instructor", "Instructor"),
        ("student", "Student"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    def is_admin(self):
        return self.role == "admin" or self.is_superuser

    def is_instructor(self):
        return self.role == "instructor" or self.is_staff

    def is_student(self):
        return self.role == "student"
