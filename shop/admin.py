from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display=('name' , 'image' , 'description','status','created_at')

class ProductAdmin(admin.ModelAdmin):
    list_display=('category','name','vendor','product_image','quantity','original_price','selling_price','description','status','trending')

admin.site.register(Category , CategoryAdmin)
admin.site.register(Product,ProductAdmin)