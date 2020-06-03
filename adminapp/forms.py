from django import forms

from authapp.models import ShopUser
from authapp.forms import ShopUserChangeForm
from mainapp.models import ProductCategory, Product
from django.forms import ModelChoiceField



#
class ShopUserAdminEditForm(ShopUserChangeForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


#
class ProductCategoryEditForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

        # we need to show in form available categories from db
        self._category = forms.ModelChoiceField(queryset=ProductCategory.objects.all())
        self.fields['category'] = self._category


