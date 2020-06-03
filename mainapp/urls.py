from django.urls import path, re_path, include

import mainapp.views as mainapp


app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', mainapp.products, name='index'),  # show products

    # show products for category_id=4
    # products/4
    path('<int:pk>', mainapp.products, name='category'),

    # show details of product with id=3
    # products/product/3
    path('product/<int:pk>/', mainapp.product, name='product'),
]

