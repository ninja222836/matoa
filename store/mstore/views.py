from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
import random

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView

from mstore.forms import RegisterUserForm, LoginUserForm, QuantityForm
from mstore.models import Product, ProductImage, ProductCategory, ProductScheme, Order, OrderItem  # FavouriteProduct
from mstore.utils import cart_add_util


def home(request):
    products = Product.objects.filter(is_published=True)

    products_for_slider = products.exclude(description_for_slider__isnull=True).exclude(
        description_for_slider__exact='')

    monthly_deals = products.filter(category__name='Watches').order_by('-time_create')[:4]

    products_maple = products.filter(model='MAPLE')[:3]
    products_ebony = products.filter(model='EBONY')[:3]
    products_featured = products.filter(model='FEATURED')[:3]
    return render(request, 'mstore/home.html', {'title': 'Homepage',
                                                'products_for_slider': products_for_slider,
                                                'monthly_deals': monthly_deals,
                                                'products_maple': products_maple,
                                                'products_ebony': products_ebony,
                                                'products_featured': products_featured,

                                                })


def search(request):
    if request.method == 'GET':
        return redirect(reverse('Search Results'))
    return render(request, 'mstore/search.html')


def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_images = ProductImage.objects.filter(product=product)
    product_scheme = ProductScheme.objects.filter(product=product).first()
    quantity_form = QuantityForm

    products = list(Product.objects.filter(model=product.model, category=product.category).exclude(pid=product.pid))
    if len(products) >= 4:
        related_products = random.sample(products, 4)
    else:
        related_products = products

    return render(request, 'mstore/product.html', {'title': product.name,
                                                   'product': product,
                                                   'product_images': product_images,
                                                   'related_products': related_products,
                                                   'product_scheme': product_scheme,
                                                   'quantity_form': quantity_form, })


def product_list(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    products = Product.objects.filter(is_published=True, category=category)

    return render(request, 'mstore/watches.html', {'title': category.name,
                                                   'category': category,
                                                   'products': products, })


class SearchView(ListView):
    model = Product
    template_name = 'mstore/watches.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("search")

        if query is not None:
            object = Product.objects.filter(
                Q(name__icontains=query)
            )

        context['title'] = 'Results'
        context['products'] = object
        context['search'] = query
        context['text'] = f'Results to "{query}":'
        return context


def search_tab(request):
    search_text = request.GET.get('search')
    if not search_text:
        search_text = ""

    if len(search_text) != 0:
        results = Product.objects.filter(name__icontains=search_text)
    else:
        results = None

    context = {'results': results}

    return render(request, 'mstore/search_results.html', context)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'mstore/register.html'
    success_url = reverse_lazy('Login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registration'
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'mstore/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


def add_to_cart(request, slug):
    if request.user.is_anonymous:
        return JsonResponse('You are not registered!', safe=False)

    orderItem = cart_add_util(request, slug)[0]

    orderItem.quantity += 1

    orderItem.save()
    print(f"Item {orderItem} was added successfully")
    return JsonResponse('', safe=False)


def add_product_page(request, slug):
    quantity = request.POST.get('quantity')

    orderItem = cart_add_util(request, slug)[0]

    orderItem.quantity += int(quantity)

    orderItem.save()

    print("true")
    return HttpResponse("OK")


def cart(request):
    if request.user.is_anonymous:
        return render(request, 'mstore/cart_products.html', {'cart_products': None,
                                                             'order': None, })

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    cart_products = OrderItem.objects.filter(order=order)
    print(cart_products)

    return render(request, 'mstore/cart_products.html', {'cart_products': cart_products,
                                                         'order': order, })


def update_cart(request, slug, button_value):
    action = button_value
    print('Action', action)

    util_data = cart_add_util(request, slug)
    print(util_data)
    orderItem = util_data[0]
    order = util_data[1]

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    elif action == 'delete':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    cart_products = OrderItem.objects.filter(order=order)

    return render(request, 'mstore/cart_products.html', {'cart_products': cart_products,
                                                         'order': order, })


def favourites(request):
    customer = request.user.customer

    favourite_products = {}
    return render(request, 'mstore/watches.html', {'title': 'Favourite Products',
                                                   'products': favourite_products,
                                                   'text': 'Your favourite products', })


def add_to_favourites(request, slug):
    product = get_object_or_404(Product, slug=slug)
    customer = request.user.customer
    if product.favourites.filter(id=customer.id).exists():
        product.favourites.remove(customer)
        print("removed", product.favourites.all())
        liked = False

    else:
        product.favourites.add(customer)
        print("added", product.favourites.all())
        liked = True

    return render(request, 'mstore/liked_card.html', {'liked': liked})


def checkout(request):
    return render(request, 'mstore/checkout.html', {'title': 'Checkout'})


def payment(request):
    return render(request, 'mstore/payment.html', {'title': 'Payment'})


def logout_user(request):
    logout(request)
    return redirect('Home')
