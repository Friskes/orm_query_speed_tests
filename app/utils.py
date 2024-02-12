import time
import functools
import statistics

from django.db import connection, reset_queries

from app.models import FirstModel, SecondModel


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        firsts_ids = FirstModel.objects.values_list("id", flat=True)

        reset_queries()

        all_execution_time = []
        for _ in range(10):  # замер состоит из 10 тестов

            start_queries = len(connection.queries)
            start = time.perf_counter()

            res = func(*args, **kwargs, firsts_ids=firsts_ids)

            end = time.perf_counter()
            end_queries = len(connection.queries)

            execution_time = end - start
            all_execution_time.append(execution_time)
            print(
                f"Function name: {func.__name__}   "
                f"Queries quantity: {end_queries - start_queries}   "
                f"Execution time: {(execution_time):.2f}s"
            )

        print(f"\nMedian is: {statistics.median(all_execution_time):.2f}s")

        # return res

    return inner_func
