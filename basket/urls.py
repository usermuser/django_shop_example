from django.urls import path

from basket import views as basket

app_name = 'basket'

urlpatterns = [
    path('', basket.basket, name='view'),
    path('add/<int:pk>/', basket.basket_add, name='add'),
    path('remove/<int:pk>/', basket.basket_remove, name='remove'),
    path('edit/<int:pk>/<int:quantity>/', basket.basket_edit, name='edit')
]
