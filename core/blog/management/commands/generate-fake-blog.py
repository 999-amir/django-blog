from django.core.management.base import BaseCommand
from faker import Faker

from blog.models import CategoryModel, BlogModel, BlogContentModel
from home.models import CostumeUser


class Command(BaseCommand):
    help = "this function will generate fake blog [ used for dev ]"

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

        category = CategoryModel.objects.filter(name="fake-category")
        if category.exists():
            category = category.first()
        else:
            category = CategoryModel.objects.create(
                name="fake-category", color="red-600"
            )

        iteration_blog = int(
            input("#-DJANGO] how many fake-blog you want to create? -> ")
        )
        iteration_content = int(
            input(
                "#-DJANGO] how many fake-content"
                "for each fake-blog you want to create? -> "
            )
        )

        for _ in range(iteration_blog):  # create 10 objects for one-command
            blog = BlogModel.objects.create(
                user=user, title=self.faker.job(), snippet=self.faker.text()
            )
            blog.category.add(category)
            blog.save()
            for _ in range(iteration_content):
                BlogContentModel.objects.create(
                    blog=blog,
                    text=self.faker.paragraphs(),
                    file="fake-data-generator/f.jpg",
                )

        print(
            f"#-DJANGO] {iteration_blog*iteration_content}"
            f"objects has been created in database"
        )
        print(
            "#-DJANGO] you can checkout data with this "
            "user\n\tNAME: fake-data-generator\n\t"
            "EMAIL: fake@gmail.com\n\tPASSWORD: 123"
        )
