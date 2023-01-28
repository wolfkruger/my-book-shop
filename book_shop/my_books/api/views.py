from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from my_books.models import *
from .serializers import *


class BooksAPIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BooksViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Books.objects.filter(available=True)
    queryset = queryset.select_related('genre').all()
    queryset = queryset.prefetch_related('authorship').all()
    serializer_class = BooksSerializer
    pagination_class = BooksAPIListPagination


# class BooksAPIView(APIView):
#     def get(self, request):
#         books = Books.objects.filter(available=True)
#         books = books.prefetch_related('authorship').all()
#         books = books.select_related('genre').all()
#         serializer = BooksSerializer(books, many=True)
#         return Response({'books': serializer.data})
#
#
# class BookDetailAPIView(APIView):
#     def get(self, request, pk=None):
#         books = Books.objects.filter(available=True)
#         book = get_object_or_404(books, pk=pk)
#         serializer = BooksSerializer(book, many=False)
#         return Response({'book': serializer.data, 'add_to_cart': reverse_lazy('add_to_my_cart_api', args=[pk], request=request)})


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.validated_data})


# class CartAPIView(APIView):
#     def get(self, request):
#         cart = Cart.objects.filter(user=self.request.user)
#         return Response({'cart': CartSerializer(cart, many=True).data})


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, )
    #authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user)
        queryset = queryset.prefetch_related('authorship').all()
        return queryset

    def create(self, request, *args, **kwargs):
        books = Books.objects.filter(available=True)
        #books = books.prefetch_related('authorship').all()
        #books = books.select_related('genre').all()
        book = get_object_or_404(books, pk=kwargs.get('pk'))
        cart = Cart.objects.filter(user=self.request.user)
        cart = cart.prefetch_related('authorship').all()
        serializer = CartSerializer(data=request.data)
        added = False
        if serializer.is_valid():
            if cart:
                for item in cart:
                    if item.book == book:
                        item.quantity += 1 if item.quantity < book.number else 0
                        added = True
                        item.save()
                        return Response({'added_book': CartSerializer(item, many=False).data})
            if not cart or not added:
                cart = Cart(
                    book=book,
                    quantity=serializer.validated_data['quantity'],
                    user=self.request.user
                )
                cart.save()
                for author in book.authorship.all():
                    cart.authorship.add(author)
                cart.save()
                return Response({'added_book': CartSerializer(cart, many=False).data})
        return Response({'cart': CartSerializer(cart, many=True).data})

    def update(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)
        cart = Cart.objects.filter(user=self.request.user)
        if serializer.is_valid():
            book = get_object_or_404(Books, pk=serializer.validated_data['book'].id)
            for item in cart:
                if item.book == book:
                    if item.quantity > 1:
                        item.quantity -= 1
                        item.save()
                    else:
                        item.delete()
        cart = Cart.objects.filter(user=self.request.user)
        return Response({'cart': CartSerializer(cart, many=True).data})

    def destroy(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)
        cart = Cart.objects.filter(user=self.request.user)
        if serializer.is_valid():
            for item in cart:
                item.delete()
        cart = Cart.objects.filter(user=self.request.user)
        return Response({'cart': CartSerializer(cart, many=True).data})


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Orders.objects.filter(user=self.request.user)
        queryset = queryset.select_related('books').all()
        queryset = queryset.prefetch_related('authorship').all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        cart = Cart.objects.filter(user=self.request.user)
        cart = cart.select_related('book').all()
        cart = cart.prefetch_related('authorship').all()
        if serializer.is_valid():
            book = get_object_or_404(Books, id=serializer.validated_data['books'].id)
            for item in cart:
                if item.book == book:
                    book_in_cart = cart.get(book=item.book)
                    order = Orders(
                        books=book,
                        user=self.request.user,
                        quantity=book_in_cart.quantity,
                        total_price=book.price * book_in_cart.quantity
                    )
                    order.save()
                    for author in book.authorship.all():
                        order.authorship.add(author)
                    order.save()
                    book_in_cart.delete()
                    return Response({'order': OrderSerializer(order, many=False).data})
        return Response({'order': 'Order is none'})

