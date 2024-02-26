import re
from django.db import models
from django_extensions.db.models import TimeStampedModel
from apps.account.models import Account
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_field(value):
    if not value:
        raise ValidationError(
            _("%(value) should not be null"),
            params={"value": value},
        )
    elif value and not re.match(r'^[a-zA-Z]+$', value):
        raise ValidationError(
            'Name should not have numbers'
        )

# Create your models here.


class Script(TimeStampedModel):

    Smoke = 'smoke'
    Soak = 'soak'
    Performance = 'performance'

    Development = 'Development'
    Ready = 'Ready'
    Completed = 'Completed'

    CATEGORY_CHOICES = (
        (Smoke, 'Smoke'),
        (Soak, 'Soak'),
        (Performance, 'Performance')
    )

    STATUS_CHOICES = (
        (Development, 'IN Development'),
        (Ready, 'Ready'),
        (Completed, 'Completed')
    )

    name = models.CharField(max_length=200, unique=True, validators=[validate_field])
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50, blank=False, null=False)
    owner = models.ForeignKey(Account, on_delete=models.PROTECT, blank=False, null=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name
