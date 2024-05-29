from django.core.management.base import BaseCommand
import schedule
import time
from datetime import datetime

from django.utils import timezone

from boxes.models import Box  # Adjust the import path as needed


class Command(BaseCommand):
    help = 'Starts and runs the task scheduler indefinitely'

    def handle(self, *args, **options):
        def unlock_boxes():
            boxes_to_unlock = Box.objects.filter(date_opening__lte=datetime.now(), status=Box.Statuses.LOCKED)
            for box in boxes_to_unlock:
                if timezone.now() >= box.date_opening:
                    box.status = Box.Statuses.OPENED
                    box.save()
                    self.stdout.write(self.style.SUCCESS(f'Box {box.name} has been unlocked.'))

        schedule.every().minute.do(unlock_boxes)

        while True:
            schedule.run_pending()
            time.sleep(1)
