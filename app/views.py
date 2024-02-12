from django.db import transaction

from app.utils import query_debugger
from app.models import FirstModel, SecondModel

# Create your views here.

# python manage.py shell
# from app.views import test1, test2, test3
# test1()
# CTRL+Z+ENTER


@query_debugger
def test1(firsts_ids):  # Median is: 1.50s

    with transaction.atomic():
        for _id in firsts_ids:
            model_obj = FirstModel.objects.get(id=_id)
            related_obj = model_obj.related_model.get(flag=True)
            related_obj.text = model_obj.text + "!"
            related_obj.save()


@query_debugger
def test2(firsts_ids):  # Median is: 1.81s

    objects = []
    for _id in firsts_ids:
        model_obj = FirstModel.objects.get(id=_id)
        related_obj = model_obj.related_model.get(flag=True)
        related_obj.text = model_obj.text + "!"
        objects.append(related_obj)
    with transaction.atomic():
        for rel_obj in objects:
            rel_obj.save()


@query_debugger
def test3(firsts_ids):  # Median is: 1.66s

    objects = []
    for _id in firsts_ids:
        model_obj = FirstModel.objects.get(id=_id)
        related_obj = model_obj.related_model.get(flag=True)
        related_obj.text = model_obj.text + "!"
        objects.append(related_obj)
    SecondModel.objects.bulk_update(objects, ['text'])











from django.db import transaction

# python manage.py shell
# from app.views import test_trans
# test_trans()
# CTRL+Z+ENTER

def test_trans():
    FirstModel.objects.filter(text="Hi").delete()

    with transaction.atomic():
        transaction_save_id = transaction.savepoint()

        print(FirstModel.objects.filter(text="Hi"))
        FirstModel.objects.create(text="Hi")
        print(FirstModel.objects.filter(text="Hi"))
        # transaction.savepoint_rollback(transaction_save_id)

    print(FirstModel.objects.filter(text="Hi"))
    transaction.savepoint_rollback(transaction_save_id)
    print(FirstModel.objects.filter(text="Hi"))
