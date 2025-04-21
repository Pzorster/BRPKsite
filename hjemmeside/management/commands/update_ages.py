from django.core.management.base import BaseCommand
from django.db.models import F
from hjemmeside.models import Medlem
from django.utils import timezone

class Command(BaseCommand):
    help = 'Updates the age of all members based on their birth date'

    def handle(self, *args, **options):
        # In the future consider if you want to remove the count and its subsequent printout. Consider how you want to log that happening.
        count = 0
        for medlem in Medlem.objects.all():
            old_age = medlem.alder
            
            # Calculate new age
            today = timezone.now().date()
            born = medlem.fodt_ar
            new_age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            
            # Only update if age has changed
            if old_age != new_age:
                medlem.alder = new_age
                medlem.save(update_fields=['alder'])
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} member ages'))