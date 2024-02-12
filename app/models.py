from django.db import models

# Create your models here.


class FirstModel(models.Model):
    text = models.TextField(max_length=99999999999)


class SecondModel(models.Model):
    text = models.TextField(max_length=99999999999)
    flag = models.BooleanField()
    first = models.ForeignKey(
        FirstModel,
        related_name="related_model",
        on_delete=models.CASCADE
    )
