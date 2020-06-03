from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя',
                            max_length=55,
                            unique=True)
    description = models.TextField(verbose_name='описание',
                                   blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    class Meta:
        ordering = ['name',]
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory,
                                 on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя продукта',
                            max_length=128)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    short_desc = models.CharField(verbose_name='краткое описание продукта',
                                  max_length=60,
                                  blank=True)
    description = models.TextField(verbose_name='описание продукта',
                                   blank=True)
    price = models.DecimalField(verbose_name='цена продукта',
                                max_digits=8,
                                decimal_places=2,
                                default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе',
                                           default=0)

    class Meta:
        ordering = ['category']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return '{} {}'.format(self.name, self.category.name)
