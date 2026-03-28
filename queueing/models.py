from django.db import models
from django.conf import settings
from branches.models import Branch
from services.models import Service
from counters.models import Counter


class Ticket(models.Model):
    class ClientType(models.TextChoices):
        REGULAR  = 'regular',  'Regular'
        PWD      = 'pwd',      'PWD'
        SENIOR   = 'senior',   'Senior Citizen'
        PREGNANT = 'pregnant', 'Pregnant'

    class Status(models.TextChoices):
        WAITING   = 'waiting',   'Waiting'
        SERVING   = 'serving',   'Serving'
        COMPLETED = 'completed', 'Completed'
        NO_SHOW   = 'no_show',   'No Show'

    PRIORITY_MAP = {
        ClientType.PWD:      1,
        ClientType.SENIOR:   2,
        ClientType.PREGNANT: 3,
        ClientType.REGULAR:  4,
    }

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    counter = models.ForeignKey(
        Counter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets'
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets'
    )
    ticket_number = models.CharField(max_length=10)
    client_type = models.CharField(
        max_length=10,
        choices=ClientType.choices,
        default=ClientType.REGULAR
    )
    priority = models.PositiveIntegerField(default=4)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.WAITING
    )
    is_pre_registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    called_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.ticket_number} - {self.status}"

    def save(self, *args, **kwargs):
        # Automatically set priority based on client type before saving
        self.priority = self.PRIORITY_MAP.get(
            self.client_type,
            4
        )
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['priority', 'created_at']