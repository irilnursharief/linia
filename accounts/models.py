from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        STAFF = "staff", "Staff"
        CLIENT = "client", "Client"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    branch = models.ForeignKey(
        "branches.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_staff_member(self):
        return self.role == self.Role.STAFF

    @property
    def is_client(self):
        return self.role == self.Role.CLIENT
