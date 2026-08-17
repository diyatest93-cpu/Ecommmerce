from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import *
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
import random
from django.core.mail import send_mail

# Create your views here.
def rergistration(request):

    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        if User.objects.filter(email__iextact=email).exists():
            messages.error(request, "Email already Exists")

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')
    
    return render(request, 'myapp/index.html')

def admin_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid')

    return render(request, 'myapp/login.html')
def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)

            # Generate 6 digit OTP
            otp = str(random.randint(100000, 999999))

            # Store OTP and email in session
            request.session["reset_email"] = email
            request.session["reset_otp"] = otp

            # Send OTP to email
            send_mail(
                subject="Password Reset OTP",
                message=f"""
Hello {user.username},

Your OTP for resetting your password is:

{otp}

This OTP is valid for this password reset request.

If you did not request a password reset, please ignore this email.
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(
                request,
                "OTP has been sent to your email."
            )

            return redirect("verify_otp")

        except User.DoesNotExist:

            messages.error(
                request,
                "No account found with this email."
            )

    return render(request, "myapp/forgot_password.html")


# ---------------- VERIFY OTP ----------------

def verify_otp(request):

    if "reset_email" not in request.session:
        return redirect("forgot_password")

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        saved_otp = request.session.get("reset_otp")

        if entered_otp == saved_otp:

            # OTP verified
            request.session["otp_verified"] = True

            return redirect("reset_password")

        else:

            messages.error(
                request,
                "Invalid OTP. Please try again."
            )

    return render(request, "myapp/verify_otp.html")


def reset_password(request):

    # User must verify OTP first
    if not request.session.get("otp_verified"):
        return redirect("forgot_password")

    if request.method == "POST":

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check password match
        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return render(
                request,
                "reset_password.html"
            )

        # Get email from session
        email = request.session.get("reset_email")

        try:

            user = User.objects.get(email=email)

            # Set new password
            user.set_password(password)
            user.save()

            # Clear reset session
            request.session.pop("reset_email", None)
            request.session.pop("reset_otp", None)
            request.session.pop("otp_verified", None)

            messages.success(
                request,
                "Password reset successfully. Please login."
            )

            return redirect("user_login")

        except User.DoesNotExist:

            messages.error(
                request,
                "User not found."
            )

    return render(request, "myapp/reset_password.html")
@login_required
def dashboard(request):

    total_users = User.objects.count()
    total_categories = category.objects.count()
    total_subcategories = subcategory.objects.count()
    total_thirdcategories = thirdcategory.objects.count()
    total_products = product.objects.count()
    total_orders = Order.objects.count()

    total_revenue = 0

    orders = Order.objects.all()

    for order in orders:
        total_revenue += order.total_amount

    context = {
        'total_users': total_users,
        'total_categories': total_categories,
        'total_subcategories': total_subcategories,
        'total_thirdcategories': total_thirdcategories,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
    }

    return render(request, 'myapp/admin_dashboard.html', context)

def add_category(request):
    if request.method=="POST":
        
        form=categoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('category_list') 
    else:
        form=categoryForm()

    
    return render(request, 'myapp/add_category.html', {'form':form})
def category_list(request):

    query = request.GET.get('q', '').strip()

    data = category.objects.filter(
        category_name__icontains=query
    )

    return render(request, 'myapp/category_list.html', {
        'data': data,
        'query': query
    })
def user_logout(request):
    logout(request)
    return redirect('login')
def edit_category(request, id):
    obj=get_object_or_404(category, id=id)

    if request.method=="POST":
        form=categoryForm(request.POST, request.FILES,instance=obj)

        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated successfully")
            return redirect('category_list')
    else:
        form=categoryForm(instance=obj)
    return render(request, 'myapp/edit_category.html', {'form':form})
def delete_category(request, id):
    obj=get_object_or_404(category, id=id)
    obj.delete()
    messages.success(request, "category deleted successfully")
    return redirect('category_list')

def add_subcategory(request):
    if request.method=="POST":

        form=subcategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "subcategory added successfully!")
            return redirect('add_subcategory')

    else:
        form=subcategoryForm()
    return render(request, 'myapp/add_subcategory.html', {'form':form})      
def subcategory_list(request):

    query = request.GET.get('q', '').strip()

    data = subcategory.objects.filter(
        subcategory_name__icontains=query
    )
    paginator = Paginator(data, 5)  # 5 records per page
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)


    return render(request, 'myapp/subcategory_list.html', {
        'data': data,
        'query': query
    })
def edit_subcategory(request, id):
    obj=get_object_or_404(subcategory, id=id)

    if request.method=="POST":
        form=subcategoryForm(request.POST, request.FILES,instance=obj, )
        if form.is_valid():
            form.save()
            messages.success(request, "subcategory Updated Successfully")
            return redirect('subcategory_list')
    else:
        form=subcategoryForm(instance=obj)
    return render(request, 'myapp/edit_subcategory.html', {'form':form})  

def delete_subcategory(request, id):
    data=get_object_or_404(subcategory, id=id)
    data.delete()
    messages.success(request, 'product deleted successfully!')
    return redirect('subcategory_list')

def add_thirdcategory(request):
    if request.method=="POST":
        form=thirdcategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thirdcategory Added successfully!')
            return redirect('thirdcategory_list')
    else:
        form=thirdcategoryForm()
    return render(request, 'myapp/add_thirdcategory.html', {'form':form})    

def thirdcategory_list(request):

    query = request.GET.get('q', '').strip()

    data = thirdcategory.objects.filter(
        thirdcategory_name__icontains=query
    )
    paginator = Paginator(data, 5)  
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)

    return render(request, 'myapp/thirdcategory_list.html', {
        'data': data,
        'query': query
    })

def edit_thirdcategory(request, id):
    obj=get_object_or_404(thirdcategory, id=id)

    if request.method=="POST":
        form=thirdcategoryForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Updated Successfully!")
            return redirect('thirdcategory_list')
    else:
        form=thirdcategoryForm(instance=obj)
    return render(request, 'myapp/edit_thirdcategory.html', {'form':form})   

def delete_thirdcategory(request, id):
    obj=get_object_or_404(thirdcategory, id=id)
    obj.delete()
    messages.success(request, 'Product deleted Successfully !')
    return redirect('thirdcategory_list')

def add_product(request):
    if request.method=="POST":
        form=productForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "product added Successfully!")
            return redirect('product_list')
    else:
        form=productForm()
    return render(request, 'myapp/add_product.html', {'form':form})        

def product_list(request):

    query = request.GET.get('q', '')
    print("SEARCH QUERY=", query)

    data = product.objects.filter(
        Q(pname__icontains=query) |
        Q(brand__icontains=query) |
        Q(p_detail__icontains=query)
        
    )
    paginator=Paginator(data,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    
    return render(request, 'myapp/product_list.html', {
        'data': data,
        'query': query,
        'page_obj':page_obj
    })
@login_required
def admin_orders(request):

    orders = Order.objects.all().order_by('-created_at')

    return render(request, 'myapp/admin_orders.html', {
        'orders': orders
    })
@login_required
def admin_order_detail(request, order_id):

    order = Order.objects.get(id=order_id)

    order_items = OrderItem.objects.filter(order=order)
    reviews = Review.objects.filter(
    product__in=[item.product for item in order_items],
    user=order.user
)

    return render(request, 'myapp/admin_order_detail.html', {
        'order': order,
        'order_items': order_items,
        'reviews':reviews
    })

def edit_product(request, id):
    obj=get_object_or_404(product, id=id)
    if request.method=="POST":
        form=productForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            print('updated')
            messages.success(request, "Product Updated Successfully!")
            return redirect('product_list')
        else:
            print(form.errors)
    else:
        form=productForm(instance=obj)
    return render(request, 'myapp/edit_poduct.html', {'form':form})        

def delete_product(request, id):
    obj=get_object_or_404(product, id=id)
    obj.delete()
    messages.success(request, "product Deleted Successfully!")
    return redirect('product_list')

def get_subcategory(request):
    category_id=request.GET.get('category_id')
    subcategories=subcategory.objects.filter(category_id=category_id)

    data=[]
    for i in subcategories:
        data.append({
            'id':i.id,
            'name':i.subcategory_name
        })
    return JsonResponse(data, safe=False)  

def get_thirdcategory(request):
    subcategory_id=request.GET.get('subcategory_id')
    thirdcategories=thirdcategory.objects.filter(subcategory_id=subcategory_id)
    data=[]
    for i in thirdcategories:
        data.append({
            'id':i.id,
            'name':i.thirdcategory_name
        }) 
    return JsonResponse(data,safe=False)    

def add_banner(request):
    if request.method=="POST":
        form=bannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image Uploaded!')
            return redirect('banner_list')
    else:
        form=bannerForm()
    return render(request, 'myapp/add_banner.html', {'form':form}) 
def banner_list(request):
    data=banner.objects.all()
    return render(request, 'myapp/banner_list.html', {'data':data})   
def edit_banner(request, id):

    data = get_object_or_404(banner, id=id)

    if request.method == "POST":
        form = bannerForm(request.POST, request.FILES, instance=data)

        if form.is_valid():
            form.save()
            messages.success(request, "Banner updated successfully!")
            return redirect('banner_list')

    else:
        form = bannerForm(instance=data)

    return render(request, 'myapp/edit_banner.html', {
        'form': form
    })

def delete_banner(request, id):

    data = get_object_or_404(banner, id=id)
    data.delete()

    messages.success(request, "Banner deleted successfully!")
    return redirect('banner_list')
    

def user_registration(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('user_login')
    return render(request, 'myapp/user_registration.html')

def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_home')
        else:
            messages.error(request, 'Invalid')
    return render(request, 'myapp/user_login.html')    
def user_home(request):
    banners=banner.objects.filter(status=True)
    categories=category.objects.filter(status=True)
    context={
            'banners':banners,
            'categories':categories
            }
    return render(request, 'myapp/user_home.html', context)

def category_page(request, id):
    cat=get_object_or_404(category, id=id)
    subcategories=subcategory.objects.filter(category=cat)

    context={
        'cat':cat,
        'subcategories':subcategories
    }
    return render(request, 'myapp/category_page.html', context)
def subcategory_page(request, id):
    sub=subcategory.objects.get(id=id)
    thirdcategories=thirdcategory.objects.filter(subcategory=sub)

    context={
        'sub':sub,
        'thirdcategories':thirdcategories
    }
    return render(request, 'myapp/subcategory_page.html', context)

def user_product_list(request, id):

    thirdcat = thirdcategory.objects.get(id=id)

    products = product.objects.filter(thirdcategory=thirdcat)

    context = {
        'thirdcat': thirdcat,
        'products': products
    }

    return render(request, 'myapp/user_product_list.html', context)
def view_product(request, id):
    data = product.objects.get(id=id)

    related_products = product.objects.filter(
        category=data.category
    ).exclude(id=data.id)[:4]

    reviews = Review.objects.filter(
        product=data
    ).order_by('-created_at')

    review_form = ReviewForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            review_form = ReviewForm(request.POST)

            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = data
                review.user = request.user
                review.save()

                return redirect('view_product', id=id)

    return render(
        request,
        'myapp/product_detail.html',
        {
            'data': data,
            'related_products': related_products,
            'reviews': reviews,
            'review_form': review_form,
        }
    )

def add_to_cart(request, id):
    data=get_object_or_404(product, id=id)
    cart_item, created=cart.objects.get_or_create(user=request.user, product=data)

    if not created:
        cart_item.quantity+=1
        cart_item.save()
        messages.success(request, "product Added to cart successfully!")
    return redirect('product_detail', id=id)    
@login_required
def cart_page(request):
    cart_items = cart.objects.filter(user=request.user, status=True)

    total = 0

    for item in cart_items:
        total += item.total_price

    return render(request, 'myapp/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def increase_qun(request, id):
    cart_item=get_object_or_404(cart,id=id, user=request.user)
    cart_item.quantity+=1
    cart_item.save()
    return redirect('cart')


@login_required
def decrease_qun(request, id):
    cart_item=get_object_or_404(cart,id=id, user=request.user)
    if cart_item.quantity >1:

        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()    
    return redirect('cart')

def remove_cart(request, id):
    cart_item=get_object_or_404(cart, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = cart.objects.filter(user=request.user, status=True)

    total = 0
    for items in cart_items:
        total += items.total_price

    if request.method == "POST":
        print("POST REQUEST AAVI")

        form = addressForm(request.POST)

        if form.is_valid():
                print("FORM VALID CHE")

                address = form.save(commit=False)
                address.user = request.user
                address.save()

                print("ADDRESS SAVE THAYO")

                messages.success(request, "Address Saved Successfully!")
                return redirect('place_order')

        else:
            print(form.errors)

    else:
        form = addressForm()

    return render(request, 'myapp/checkout.html', {
            'form': form,
            'cart_items': cart_items,
            'total': total
        })

@login_required
def place_order(request):

        # User na cart items levana
        cart_items = cart.objects.filter(user=request.user, status=True)

        # Cart khali che ke nai check karvu
        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect("cart")

        # User nu latest address levanu
        address = Address.objects.filter(user=request.user).last()

        # Address na hoy to checkout page par mokalvu
        if not address:
            messages.error(request, "Please add your address.")
            return redirect("checkout")

        # Total calculate karvu
        total = 0
        for item in cart_items:
            total += item.total_price

        # GET Request → Place Order page batavvi
        if request.method == "GET":
            return render(request, "myapp/place_order.html", {
                "cart_items": cart_items,
                "address": address,
                "total": total,
            })

        # POST Request → Order Place karvo
        elif request.method == "POST":
            print('post requset avii')
            payment_method=request.POST.get('payment_method')

            # Order create karvo
            order = Order.objects.create(
                user=request.user,
                address=address,
                total_amount=total,
                payment_method=payment_method,
                payment_status="pending"
            )

            # OrderItem create karva
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

                # Stock update karvu
                item.product.stock -= item.quantity
                item.product.save()

            # Cart empty karvi
            cart_items.delete()

            messages.success(request, "Order placed successfully!")

            return redirect("order_success")

@login_required
def order_success(request):
    return render(request, 'myapp/order-success.html')

def profile(request):
    context={
            'user':request.user
        }
    return render(request, 'myapp/profile.html', context)

def myorders(request):
    orders=Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'myapp/my_orders.html',{'orders':orders})

@login_required
def order_detail(request, order_id):
    order=Order.objects.get(id=order_id, user=request.user)
    order_items=OrderItem.objects.filter(order=order)

    return render(request, 'myapp/order_detail.html',{'order':order, 'order_items':order_items})

def search_products(request):
    query=request.GET.get('q', '').strip()
    products=product.objects.filter(Q(pname__icontains=query)|
                                    Q(brand__icontains=query)|
                                    Q(p_detail__icontains=query), status=True)
    return render(request, 'myapp/search_items.html', {'products':products, 'query':query})

        



