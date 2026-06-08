from django.contrib.auth.models import AbstractUser

from django.db import models

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ("superadmin", "Super Admin"),
        ("teacher", "Teacher"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="teacher"
    )

    # created_at = models.DateTimeField(
    #     auto_now_add=True
    # )

    def __str__(self):
        return self.username



class Student(models.Model):

    FEE_STATUS_CHOICES = (
        ("Paid", "Paid"),
        ("Pending", "Pending"),
    )

    excel_file = models.ForeignKey(
        "ExcelUpload",
        on_delete=models.CASCADE,
        related_name="students",
        null=True,
        blank=True
    )

    roll_no = models.CharField(max_length=50)

    name = models.CharField(max_length=255)

    std = models.CharField(max_length=20)

    fee_status = models.CharField(
        max_length=20,
        choices=FEE_STATUS_CHOICES,
        default="Pending"
    )

    remaining_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_paid_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.roll_no} - {self.name}"


class ExcelUpload(models.Model):

    file = models.FileField(upload_to="uploads/excel/")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class ChatHistory(models.Model):

    question = models.TextField()

    answer = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]
