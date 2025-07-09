import logging
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Mailings, AttemptSend, Client
from mailings_message.models import Message


def send_message(pk, request=None):
    """ Отправляет рассылку по требованию """
    try:

        mailing = Mailings.objects.get(pk=pk)
    except Mailings.DoesNotExist:

        return False

    now = timezone.now()


    if now < mailing.start_time:

        AttemptSend.objects.create(
            mailing=mailing,
            status='failed',
            server_response=(
                f"Время рассылки еще не наступило "
                f"(начало: {mailing.start_time}, сейчас: {now})"
            )
        )

        return False

    if mailing.end_time and now > mailing.end_time:

        mailing.status = 'completed'
        mailing.save()


        AttemptSend.objects.create(
            mailing=mailing,
            status='failed',
            server_response=(
                f"Время рассылки истекло "
                f"(окончание: {mailing.end_time}, сейчас: {now})"
            )
        )

        return False


    clients = mailing.clients.all()
    if not clients:

        AttemptSend.objects.create(
            mailing=mailing,
            status='failed',
            server_response="Нет получателей рассылки"
        )

        return False

    subject = mailing.message.subject
    body = mailing.message.body

    recipient_list = [client.email for client in clients]

    success_count = 0
    error_count = 0

    for client in clients:
        try:

            send_mail(
                subject=subject,
                message=body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False,
            )

            AttemptSend.objects.create(
                mailing=mailing,
                status='success',
                server_response="Письмо успешно отправлено"
            )
            success_count += 1

        except Exception as e:
            AttemptSend.objects.create(
                mailing=mailing,
                status='failed',
                server_response=str(e)
            )
            error_count += 1

    if mailing.status == 'created' and success_count > 0:
        mailing.status = 'started'
        mailing.save()

    return success_count > 0