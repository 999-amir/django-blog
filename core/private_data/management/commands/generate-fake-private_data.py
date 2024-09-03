from django.core.management.base import BaseCommand
from faker import Faker

from private_data.models import PrivateDataModel
from home.models import CostumeUser


class Command(BaseCommand):
    help = 'this function will generate fake data [ used for dev ]'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        user = CostumeUser.objects.filter(email='fake@gmail.com')
        if user.exists():   # get or create specific-user to check it easily
            user = user.first()
        else:
            user = CostumeUser.objects.create_superuser(email='fake@gmail.com', name='fake-data-generator', password='123')
            user.is_verify = True
            user.save()

        for _ in range(10):     # create 10 objects for one-command
            PrivateDataModel.objects.create(user=user, title=self.faker.job(), username=self.faker.user_name(), password=self.faker.password(), text=self.faker.text())
