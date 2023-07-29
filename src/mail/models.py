from django.db import models


class TimestampAbstractModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Letter(TimestampAbstractModel):
    class StatusChoices(models.IntegerChoices):
        PENDING = 0
        SENT = 1
        ERROR = 2

    from_email = models.CharField(max_length=256)
    recipient = models.CharField(max_length=256)
    subject = models.CharField(max_length=256)
    message = models.TextField()
    status = models.PositiveSmallIntegerField(default=StatusChoices.PENDING, choices=StatusChoices.choices)
