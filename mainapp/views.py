from django.shortcuts import render
from django.urls import resolve
from django.http import HttpResponse, HttpResponseRedirect
from .models import ProductCategory, Product
from django.shortcuts import get_object_or_404
from basket.models import Basket
import datetime
import random

now = datetime.datetime.now()
current_year = now.year


def get_hot_product():
    products = Product.objects.all()

    products_list = list(products)
    if products_list:
        _hot_product = random.choice(products_list)
    else:
        _hot_product = ['You forgot to fill db!']

    return _hot_product


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category). \
                        exclude(pk=hot_product.pk)[:3]
    return same_products


def products(request, pk=None):
    title = 'продукты'
    links_menu = ProductCategory.objects.order_by('name')
    # basket = get_basket(request.user)

    # if request.user.is_authenticated:
    #     basket = Basket.objects.filter(user=request.user)

    if pk != None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        ctx = {'title': title,
               'links_menu': links_menu,
               'category': category,
               'products': products, }

        return render(request, 'mainapp/products_list.html', ctx)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    # same_products = Product.objects.all()[3:5]

    ctx = {'title': title,
           'links_menu': links_menu,
           'hot_product': hot_product,
           'same_products': same_products,
           # 'basket': basket,
           }
    return render(request, 'mainapp/products_list.html', ctx)


def product(request, pk):
    title = 'детали'

    ctx = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
    }
    return render(request, 'mainapp/product.html', ctx)


def main(request):
    current_url = resolve(request.path_info).url_name
    title = 'Главная'

    ctx = {'title': title,
           'current_year': current_year,
           'current_url': current_url,
           'products': products,
           }
    return render(request, 'mainapp/index.html', ctx)


def contact(request):
    title = 'Контакты'

    ctx = {'title': title,
           'current_year': current_year,
           }
    return render(request, 'mainapp/contact.html', ctx)
