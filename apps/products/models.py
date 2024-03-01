from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')

    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'
    
    def __str__(self):  
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=25, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['id']

    def __str__(self):
        return self.name