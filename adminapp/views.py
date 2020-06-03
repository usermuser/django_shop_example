from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from authapp.models import ShopUser
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test
from mainapp.models import ProductCategory, Product


# R - read from CRUD
@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser',
                                                 '-is_staff', 'username')

    ctx = {
        'title': title,
        'users_list': users_list,
    }

    return render(request, 'adminapp/users.html', ctx)


# C - create from CRUD
@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    ctx = {'title': title, 'update_form': user_form}

    return render(request, 'adminapp/user_update.html', ctx)


# U - update from CRUD
@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES,
                                          instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update',
                                                args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    ctx = {'title': title, 'update_form': edit_form, }

    return render(request, 'adminapp/user_update.html', ctx)


# D - delete from CRUD
@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {'title': title, 'user_to_delete': user}

    return render(request, 'adminapp/user_delete.html', content)


# R - read from CRUD
@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categoriest_list = ProductCategory.objects.all().order_by('-name')

    ctx = {
        'title': title,
        'categories_list': categoriest_list
    }

    return render(request, 'adminapp/categories.html', ctx)


# C - create from CRUD@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'категории/создание'

    if request.method == 'POST':
        prod_cat_form = ProductCategoryEditForm(request.POST)
        if prod_cat_form.is_valid():
            prod_cat_form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
                                      # reverse('urlname')

    else:
        prod_cat_form = ProductCategoryEditForm()

    ctx = {'title': title, 'prod_cat_form': prod_cat_form}

    return render(request, 'adminapp/category_create.html', ctx)


# U - update from CRUD
@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'категории/редактирование'

    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:category_update',
                                                args=[edit_category.pk]))

    else:
        edit_form = ProductCategoryEditForm()

    ctx = {'title': title, 'edit_form': edit_form}

    return render(request, 'adminapp/category_update.html', ctx)


# D - delete from CRUD
def category_delete(request, pk):
    title = 'категории/удаление'
    category_to_delete = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_to_delete.is_active = False
        category_to_delete.save()
        return HttpResponseRedirect(reverse('admin:categories'))

    ctx = {'title': title, 'category_to_delete': category_to_delete, }
    return render(request, 'adminapp/category_delete.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):  # it's category pk!
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    ctx = {
        'title': title,
        'category': category,
        'products_list': products_list,
    }

    return render(request, 'adminapp/products.html', ctx)


def product_create(request, pk): # it's category.pk
    title = 'товар/создать'
    _category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':

        product_form = ProductEditForm(request.POST)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin:products', args=[_category.pk]))
    else:
        product_form = ProductEditForm()

    ctx = {'title': title, 'product_form': product_form, 'category': _category}
    return render(request, 'adminapp/product_create.html', ctx)


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass













