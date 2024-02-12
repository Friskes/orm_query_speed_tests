import random

from django.core.management.base import BaseCommand

from app.models import FirstModel, SecondModel


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        SecondModel.objects.all().delete()
        FirstModel.objects.all().delete()

        too_large_text = (
            "Even if you have a question that you are not sure if it's related "
            "to the Django Styleguide - just open an issue anyway. We will respond"
        ) * 200

        firsts = [FirstModel(text=f"{i} {too_large_text}") for i in range(1, 1001)]
        firsts_objs = FirstModel.objects.bulk_create(firsts)

        random.shuffle(firsts_objs)

        seconds = []
        for first in firsts_objs:

            for i in range(1, 51):
                seconds.append(
                    SecondModel(
                        text=f"{i} {too_large_text}",
                        flag=False,
                        first=first
                    )
                )
            else:
                seconds.append(
                    SecondModel(
                        text=f"{i} {too_large_text}",
                        flag=True,
                        first=first
                    )
                )

        seconds_objs = SecondModel.objects.bulk_create(seconds)
