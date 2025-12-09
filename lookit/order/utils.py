from .models import OrderItems

def reduce_stock_for_order(order_id):
    order_items = OrderItems.objects.filter(order_id=order_id)
    for item in order_items:
        item.variant.stock -= item.quantity
        item.variant.save()