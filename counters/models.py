from django.db import models
from django.conf import settings
from branches.models import Branch
from services.models import Service

class Counter(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        CLOSED = 'closed', 'Closed'
        BREAK = 'break', 'On Break'

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='counters'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='counters'
    )
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = 'counters'
    )
    number = models.PositiveIntegerField()
    status = models.CharField(
        max_length = 10,
        choices = Status.choices,
        default = Status.CLOSED
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Counter {self.number} - {self.branch.name}"
    
    class Meta:
        ordering = ['number']
        unique_together = [['branch', 'number']]