from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Reminder

class Command(BaseCommand):
    help = 'Sends out pending reminders'

    def handle(self, *args, **options):
        now = timezone.now()
        
        reminders_to_check = Reminder.objects.filter(
            is_active=True,
            time__hour=now.hour,
            time__minute=now.minute
        )

        sent_count = 0
        for reminder in reminders_to_check:
            send_notification = False
            
            if reminder.frequency == 'DAILY':
                send_notification = True
            elif reminder.frequency == 'WEEKLY':
                if now.weekday() == reminder.created_at.weekday():
                    send_notification = True
            elif reminder.frequency == 'MONTHLY':
                if now.day == reminder.created_at.day:
                    send_notification = True

            if send_notification:
                self.stdout.write(self.style.SUCCESS(
                    f"KIRIM PENGINGAT: Waktunya menabung untuk '{reminder.saving_plan.wishlist_item.name}'"
                ))
                sent_count += 1
        
        if sent_count == 0:
            self.stdout.write(self.style.WARNING(f"Waktu saat ini {now.hour}:{now.minute}. Tidak ada pengingat yang cocok."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Selesai. {sent_count} pengingat dikirim."))