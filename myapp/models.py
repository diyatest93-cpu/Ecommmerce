from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class category(models.Model):
    category_name=models.CharField(max_length=50)
    category_image=models.ImageField(upload_to ='category/', blank=True, null=True)
    status=models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

class subcategory(models.Model):
    category=models.ForeignKey(category, on_delete=models.CASCADE)
    subcategory_name=models.CharField(max_length=100)
    subcategory_image=models.ImageField(upload_to='subcategory/', blank=True, null=True)
    status=models.BooleanField(default=True)

    def __str__(self)  :
        return self.subcategory_name

class thirdcategory(models.Model):
    subcategory=models.ForeignKey(subcategory, on_delete=models.CASCADE)
    thirdcategory_name=models.CharField(max_length=100)
    thirdcategory_image=models.ImageField(upload_to='thirdcategory/', blank=True, null=True)

    status=models.BooleanField(default=True)

    def __str__(self):
        return self.thirdcategory_name    

class product(models.Model):
    category=models.ForeignKey(category, on_delete=models.CASCADE)
    subcategory=models.ForeignKey(subcategory, on_delete=models.CASCADE)
    thirdcategory=models.ForeignKey(thirdcategory, on_delete=models.CASCADE)
    pname=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    p_detail=models.TextField()
    p_image=models.ImageField(upload_to='images')
    p_rating=models.DecimalField(max_digits=2, decimal_places=1 )
    status=models.BooleanField(default=True)
    stock=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.pname

class banner(models.Model):
    b_title=models.CharField(max_length=100)
    b_detail=models.CharField(max_length=100)
    b_image=models.ImageField(upload_to='images/')
    button_text=models.CharField(max_length=20)
    button_link=models.CharField(max_length=100)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.b_title

class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    total_price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self,*args, **kwargs):
        self.total_price=self.product.price*self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}-{self.product.pname}"    


class Address(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    mobile_no=models.CharField(max_length=15)
    address=models.TextField()
    city=models.CharField(max_length=30)
    state=models.CharField(max_length=100)
    pincode=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method=models.CharField(max_length=20, default="COD")
    payment_status=models.CharField(max_length=10, default="Pending")
    status = models.CharField(max_length=50, default="Pending")


    def _str_(self):
        return f"Order {self.id}"
        

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return self.product.pname

class Review(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - {self.product.pname}"

