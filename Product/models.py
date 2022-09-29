from django.db import models
from django.urls import reverse
from accounts.models import CustomUser as User
UNIT = [('piece',"Piece"),('kg',"KG")]

def upload_to(instance, filename):
    return 'products/images/{filename}'.format(filename=filename)

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
    	ordering = ('name', )
    	verbose_name = 'category'
    	verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    unit = models.CharField(max_length=100, choices=UNIT, default="Piece")
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    image_alt = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    image_alt1 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    added_by = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    class Meta:
        ordering = ('name', )
        index_together = (('id', 'name'),)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.name])
