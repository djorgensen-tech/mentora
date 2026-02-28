from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GRADE_CHOICES = [
        ('elementary', 'Elementary (K-5)'),
        ('middle', 'Middle School (6-8)'),
        ('high', 'High School (9-12)'),
        ('college', 'College'),
    ]

    grade_level = models.CharField(max_length=20, choices=GRADE_CHOICES, blank=True)
    subjects = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Textbook(models.Model):
    GRADE_CHOICES = [
        ('elementary', 'Elementary (K-5)'),
        ('middle', 'Middle School (6-8)'),
        ('high', 'High School (9-12)'),
        ('college', 'College'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='textbooks')
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=20, choices=GRADE_CHOICES, blank=True)
    pdf_file = models.FileField(upload_to='textbooks/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.user.username})"