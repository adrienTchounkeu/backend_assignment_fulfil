import pandas as pd
import requests
import time
from celery import shared_task
from django.core.files.storage import default_storage
from django.db import IntegrityError

from backend_assignment.models import Product


@shared_task
def compute_data(file):
    print("..........Starting .............")
    send_information("Files Received ......")
    send_information("Reading File in progress ......")
    with pd.read_csv(file, header=0, chunksize=100000) as reader:
        list_products = pd.concat([chunk for chunk in reader])
        reader.close()

        print("End Lecture")
        send_information("Files Read successfully ......")

        # remove duplicates values.
        print("Deduplicating")

        send_information("Data Deduplication start......")

        list_products.drop_duplicates(subset='sku', keep='first', inplace=True)

        send_information("Data Deduplication end......")
        print("End deduplication")

        # convert to list
        list_products = list_products.values.tolist()
        send_information("Data Storing in process, please wait a few minute ......")

        # prepare for global creation : creating products objects
        list_products = map(lambda p: Product(name=p[0], sku=p[1], description=p[2]), list_products)
        print("End Mapping")
        list_products = list(list_products)
        print("End casting")

        try:
            Product.objects.bulk_create(list_products)
            print("End creating")

            send_information("Data Successfully Stored ......")
        except IntegrityError as e:
            message = "SKU duplicated values found"
        finally:
            default_storage.delete(file)


def send_information(mes):
    """
    send information to the client through socket IO.

    The route below /emit-message will perform consume a view in charge of send sockets to client
    """
    time.sleep(1)  # delay to observe client messages
    r = requests.post('http://127.0.0.1:8000/emit-message', data=dict(message=mes))
