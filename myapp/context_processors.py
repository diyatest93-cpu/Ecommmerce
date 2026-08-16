from .models import category, cart

def categories(request):
    return {'categories': category.objects.all()}


def cart_count(request):
    if request.user.is_authenticated:
        count = sum(
            item.quantity
            for item in cart.objects.filter(
                user=request.user,
                status=True
            )
        )
        return {'cart_count': count}

    return {'cart_count': 0}