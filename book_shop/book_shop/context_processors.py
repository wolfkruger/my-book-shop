from my_books.models import Cart


def len_cart(request):
    cart = Cart.objects.filter(user=request.user.is_authenticated)
    s = 0
    for i in cart:
        s += i.quantity
    return {
        'len_cart': s,
    }
