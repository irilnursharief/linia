from django.db import models

# Create your models here.
from django.db import models


class Branch(models.Model):
    name       = models.CharField(max_length=100)
    address    = models.TextField()
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Branches'
        ordering = ['name']