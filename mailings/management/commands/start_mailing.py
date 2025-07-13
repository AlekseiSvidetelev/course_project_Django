from django.core.management import BaseCommand
from mailings.models import Mailings
from mailings.services import send_mailing


class Command(BaseCommand):
    help = "Запускает рассылку по указанному ID"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки для запуска")

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        try:
            mailing = Mailings.objects.get(id=mailing_id)
            if mailing.status == Mailings.STATUS_CHOICES[0][0]:
                mailing.status = Mailings.STATUS_CHOICES[1][0]
                mailing.save()
                send_mailing(mailing_id)
                return f"Рассылка с ID {mailing_id} успешно запущена"
            else:
                return f"Рассылка с ID {mailing_id} уже запущена или завершена"
        except Mailings.DoesNotExist:
            return f"Рассылка с ID {mailing_id} не найдена"
        except Exception as e:
            return f"Ошибка: {e}"
