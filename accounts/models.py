from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        STAFF = "staff", "Staff"
        TICKETING = "ticketing", "Ticketing"
        TV_DISPLAY = "tv_display", "TV Display"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.TICKETING)
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
    def is_ticketing(self):
        return self.role == self.Role.TICKETING

    @property
    def is_tv_display(self):
        return self.role == self.Role.TV_DISPLAY
