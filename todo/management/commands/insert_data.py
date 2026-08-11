from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone

from account.models import User
from todo.models import Task

class Command(BaseCommand):
    help = "Inserting dummy data"

    def __init__(self, *args,**kwargs):
        super(Command,self).__init__(*args,*kwargs)
        self.fake = Faker()

    def handle(self, *args, **actions):
        user = User.objects.create_user(email=self.fake.email(),password="134679@xxB")

        for _ in range(20):
            Task.objects.create(
                user=user,
                title=self.fake.paragraph(nb_sentences=1),
                is_completed=random.choice([True, False])

            )