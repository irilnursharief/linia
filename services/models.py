from django.db import models
from branches.models import Branch


class Service(models.Model):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="services"
    )
    name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=5)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.branch.name} - {self.name} ({self.prefix})"

    class Meta:
        ordering = ["name"]
        unique_together = [["branch", "prefix"]]
