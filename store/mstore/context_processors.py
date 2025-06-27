from mstore.models import Order


def cart_item_count(request):
    if request.user.is_anonymous:
        return {
            'cart_item_count': 0
        }
    customer = request.user.customer
    order = Order.objects.filter(customer=customer, complete=False)[0]
    total_quantity = order.get_cart_items
    return {
        'cart_item_count': total_quantity
    }