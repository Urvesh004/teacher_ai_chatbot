from django.db import models

from excel_ai_chatbot.models import CustomUser


# Create your models here.
class UserLog(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    activity = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity}"


class SystemSettings(models.Model):

    school_name = models.CharField(max_length=255)

    system_name = models.CharField(max_length=255, default="Excel AI Chatbot")

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    address = models.TextField()

    logo = models.ImageField(upload_to="settings/", blank=True, null=True)

    def __str__(self):

        return self.school_name
