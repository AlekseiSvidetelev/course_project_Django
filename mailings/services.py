from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Mailings, AttemptSend


def send_mailing(pk, request=None):
    """Отправляет рассылку по требованию"""
    try:
        mailing = Mailings.objects.get(pk=pk)
    except Mailings.DoesNotExist:
        return False

    now = timezone.now()

    if now < mailing.start_time:
        return False

    if mailing.end_time and now > mailing.end_time:
        mailing.status = "completed"
        mailing.save()
        return False

    clients = mailing.clients.all()
    if not clients:
        return False

    subject = mailing.message.subject
    body = mailing.message.body

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
                status=True,
                server_response=f"Письмо успешно отправлено клиенту {client.email}",
                email=client,
            )
            success_count += 1

        except Exception as e:
            error_msg = f"Ошибка при отправке клиенту {client.email}: {str(e)}"

            AttemptSend.objects.create(mailing=mailing, status=False, server_response=error_msg, email=client)
            error_count += 1

    if mailing.status == "created" and success_count > 0:
        mailing.status = "started"
        mailing.save()

    return success_count > 0
