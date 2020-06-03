from django.urls import path, re_path

from authapp import views


app_name = 'authapp'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit/', views.edit, name='edit'),
    path('register/', views.register, name='register'),
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', views.verify, name='verify'),
]
