from my_books.models import Cart


def len_cart(request):
    count = Cart.objects.filter(user=request.user.is_authenticated)
    return {
        'len_cart': len(count),
    }
