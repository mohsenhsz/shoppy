from django.db import models
from accounts.models import User
from django.urls import reverse


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('shop:category', args=(self.slug,))

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discription = models.TextField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('shop:product_details', args=[str(self.pk), self.slug])

    def __str__(self):
        return self.name
