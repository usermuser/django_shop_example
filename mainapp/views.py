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
        _hot_product = random.choice(products_list) # i think its more elegant
    else:
        _hot_product = ['You forgot to fill db!']

    return _hot_product


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).\
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
            'products': products,}

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


def seed_db(request): # это код больше не нужен, делаю через management
    ProductCategory.objects.all().delete()
    Product.objects.all().delete()

    cat1 = ProductCategory()
    cat1.name = 'категория1'
    cat1.description = 'описания категории 1 бла бла бла 12314123'
    cat1.save()

    prod1 = Product()
    prod1.name = 'product1 имя'
    prod1.category = cat1
    prod1.save()

    print('[+] Created {}, {}'.format(cat1.name, prod1.name))

    cat2 = ProductCategory()
    cat2.name = 'категория22222'
    cat2.description = 'описаия егории 2 22222222222 бла 12314123'
    cat2.save()

    prod2 = Product()
    prod2.name = 'prod222222222'
    prod2.category = cat2
    prod2.save()

    print('[+] Created {}, {}'.format(cat2.name, prod2.name))
    return HttpResponse('<h1> Done! </h1> ')


# разобраться что это за хвост и либо убрать либо написать причину
# def categories(request, pk=None):
#     if pk is None:
#         return HttpResponseRedirect('/')
#     else:
#         links_menu = ProductCategory.objects.order_by('name')
#         ctx = {'links_menu': links_menu,}
#         return render(request, 'mainapp/category.html', ctx)


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
