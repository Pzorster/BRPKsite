from django.core.management.base import BaseCommand

# This needs to be schduled at some point when it's up and running. Future problem

class Command(BaseCommand):
    help = "Updates status of all activities"
    def handle(self, *args, **options):
        from hjemmeside.models import Aktivitet
        for activity in Aktivitet.objects.all():
            activity.update_status()