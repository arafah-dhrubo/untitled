import random
from django.core.management.base import BaseCommand
from faker import Faker
from goal.models import Goal
from category.models import SubCategory
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Generate fake Goal data'

    def handle(self, *args, **kwargs):
        faker = Faker()

        users = list(User.objects.all())
        subcategories = list(SubCategory.objects.all())

        if not users or not subcategories:
            self.stdout.write(
                self.style.ERROR('Users and SubCategories must exist in the database to generate fake Goals.'))
            return

        for _ in range(20):
            user = random.choice(users)
            subcategory = random.choice(subcategories)

            goal = Goal.objects.create(
                amount=faker.pydecimal(left_digits=4, right_digits=2, positive=True),
                title=faker.sentence(nb_words=6),
                description=faker.paragraph(nb_sentences=3),
                completed=faker.boolean(),
                start_date=faker.date_between(start_date='-1y', end_date='today'),
                due_date=faker.date_between(start_date='today', end_date='+1y'),
                user=user,
                category=subcategory
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created Goal: {goal.title}'))
