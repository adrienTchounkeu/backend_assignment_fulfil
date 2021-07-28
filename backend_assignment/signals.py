"""
Create post_create and post_update signals
"""

from django.dispatch import Signal, receiver

s_product_create = Signal()
s_product_update = Signal()


@receiver(s_product_create)
def product_create(sender, **kwargs):
    print("New Product Added")


@receiver(s_product_update)
def product_update(sender, **kwargs):
    print("Product Updated")
