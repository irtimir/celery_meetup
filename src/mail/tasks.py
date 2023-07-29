import random
import time
import typing
from time import sleep

from celery import shared_task
from celery.result import AsyncResult
from django.core.mail import send_mail
from django.db import transaction

from mail.models import Letter


@shared_task()
def send_email(**kwargs):
    sleep(random.choice(list(range(1, 20))))
    send_mail(**kwargs)


@shared_task()
def mass_send_email():
    letters = Letter.objects.select_for_update(skip_locked=True).filter(status=Letter.StatusChoices.PENDING)

    with transaction.atomic():
        results: typing.List[typing.Tuple[Letter, AsyncResult]] = []
        for letter in letters:
            results.append((letter, send_email.delay(
                subject=letter.subject,
                message=letter.message,
                from_email=letter.from_email,
                recipient_list=[letter.recipient],
            )))

        while any(map(lambda item: not item[1].ready(), results)):
            time.sleep(0.5)

        for letter, result in results:
            letter.status = Letter.StatusChoices.SENT if result.successful() else Letter.StatusChoices.ERROR
            letter.save()
