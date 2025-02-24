

from mstore.models import Product, Order, OrderItem
def cart_add_util(request, slug):

    product = Product.objects.get(slug=slug)

    productId = product.pid

    customer = request.user.customer
    product = Product.objects.get(pid=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    print('Id', productId)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    print(orderItem, created, orderItem.quantity)
    return orderItem, order