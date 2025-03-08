import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from hjemmeside.models import *

class Command(BaseCommand):
    # Help is printed out by terminal when you run the command
    help = "Creates DB data for testing"

    # Handle is a default function in BaseCommand that runs when you run the command
    def handle(self, *args, **kwargs):

        # Making sure there is a superuser
        user = User.objects.filter(username = "admin", is_superuser = True)
        if not user.exists():
            user = User.objects.create_superuser(username = "admin", password = "test")
        # Not sure I need this bit of code
        # else:
        #      user = user.first()

        # End 5/3: generate 1 entry into all of the fields for understanding
        # and then make chat generate a bunch more. As that is not udnerstadning, but busywork.
