from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(category)
admin.site.register(subcategory)
admin.site.register(thirdcategory)
admin.site.register(product)
admin.site.register(banner)
admin.site.register(cart)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)