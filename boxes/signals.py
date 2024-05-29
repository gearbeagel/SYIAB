from django.dispatch import receiver
from django.utils import timezone

from .models import box_unlocked, Box

@receiver(box_unlocked)
def unlock_box(sender, box_id, **kwargs):
    box = Box.objects.get(pk=box_id)
    if timezone.now() >= box.date_opening:
        box.status = Box.Statuses.OPENED
        box.save()
    print(f"Box {box.name} unlocked.")