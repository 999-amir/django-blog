from django.core.management.base import BaseCommand
from faker import Faker

from message.models import MessageModel, MessageGroupModel
from home.models import CostumeUser
from blog.models import BlogModel


class Command(BaseCommand):
    help = "this function will generate fake message [ used for dev ]"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        user = CostumeUser.objects.filter(email="fake@gmail.com")
        if user.exists():  # get or create specific-user to check it easily
            user = user.first()
        else:
            user = CostumeUser.objects.create_superuser(
                email="fake@gmail.com",
                name="fake-data-generator",
                password="El-Sueno-De-Nicos-1961-###",
            )
            user.is_verify = True
            user.save()

        blog = BlogModel.objects.create(
            user=user, title=self.faker.job(), snippet=self.faker.text()
        )
        iteration = int(
            input("#-DJANGO] how many fake-message you want to create? -> ")
        )
        group = MessageGroupModel.objects.get(blog=blog)

        for _ in range(iteration):  # create 10 objects for one-command
            MessageModel.objects.create(
                group=group, user=user, text=self.faker.text()
            )

        print(f"#-DJANGO] {iteration} objects has been created in database")
        print(
            "#-DJANGO] you can checkout data with this"
            " user\n\tNAME: fake-data-generator\n\t"
            "EMAIL: fake@gmail.com\n\tPASSWORD: 123"
        )
