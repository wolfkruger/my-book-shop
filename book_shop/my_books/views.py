from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import *
from django.views.generic import TemplateView, ListView, DetailView


class Index(TemplateView):
    template_name = 'index.html'


class BooksListView(ListView):
    model = Books
    template_name = 'my_books/books.html'
    context_object_name = 'books'
    ordering = 'title'
    paginate_by = 3

    def get_queryset(self):
        queryset = super(BooksListView, self).get_queryset()
        books = queryset.filter(available=True)
        books = books.select_related('genre').all()
        books = books.prefetch_related('authorship').all()
        title = self.request.GET.get('title')
        author = self.request.GET.get('author')
        price = self.request.GET.get('price')
        order = books.order_by(self.ordering)
        if title:
            order = books.order_by('title', 'authorship__name')
        if author:
            order = books.order_by('authorship__name', 'title')
        if price:
            order = books.order_by('price', 'title')
        return order


class BookDetailView(DetailView):
    model = Books
    template_name = 'my_books/book_detail.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data()
        if self.request.user.is_authenticated:
            items = Cart.objects.select_related('user').filter(user=self.request.user)
            items = items.select_related('book').all()
            quantity = [i for i in range(1, self.object.number + 1)]
            if items:
                for item in items:
                    if self.object == item.book:
                        quantity = [i for i in range(1, self.object.number + 1 - item.quantity)]
                        if item.quantity == self.object.number:
                            quantity = False
            context['quantity'] = quantity
        return context


class Search(ListView):
    model = Books
    paginate_by = 1
    template_name = 'my_books/search.html'
    context_object_name = 'result'

    def get_queryset(self):
        queryset = super(Search, self).get_queryset()
        data = self.request.GET.get('q')
        result = queryset.filter(Q(title__icontains=data) | Q(authorship__name__icontains=data))
        return result

    def get_context_data(self, *args, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['data'] = self.request.GET.get('q')
        return context


@login_required
def add_to_cart(request, book_id):
    items = Cart.objects.filter(user=request.user)
    book = get_object_or_404(Books, id=book_id)
    added = False
    if request.POST:
        quantity = request.POST.get('quantity')
        if items:
            for item in items:
                if item.book == book:
                    item.quantity += int(quantity)
                    added = True
                    item.save()
        if not items or not added:
            book_in_cart = Cart(
                book=book,
                quantity=int(quantity),
                user=request.user
            )
            book_in_cart.save()
            for b in book.authorship.all():
                book_in_cart.authorship.add(b)
            book_in_cart.save()
    return HttpResponseRedirect(reverse('my_cart'))


@login_required
def cart_view(request):
    my_books = Cart.objects.select_related('user').filter(user=request.user)
    context = {
        'my_books': my_books
    }
    return render(request, 'my_books/cart.html', context)


def add_and_del(request, book_id):
    items = Cart.objects.select_related('user').filter(user=request.user)
    book = get_object_or_404(Books, id=book_id)
    add = request.POST.get('add')
    delete = request.POST.get('delete')
    if add:
        for item in items:
            if item.book == book:
                if item.quantity < book.number:
                    item.quantity += 1
                    item.save()
    if delete:
        for item in items:
            if item.book == book:
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save()
                else:
                    item.delete()
    return HttpResponseRedirect(reverse('my_cart'))


def clear_cart(request):
    return render(request, 'my_books/clear_cart.html')


def confirm_clear_cart(request):
    items = Cart.objects.select_related('user').filter(user=request.user)
    for item in items:
        item.delete()
    return HttpResponseRedirect(reverse('my_cart'))


def get_order(request, book_id):
    book = Cart.objects.select_related('book').get(id=book_id)
    total_price = book.quantity * book.book.price
    context = {
        'book': book,
        'total_price': total_price,
    }
    return render(request, 'my_books/order.html', context)


def confirm_order(request, book_id):
    book = Cart.objects.select_related('book').get(id=book_id)
    total_price = book.quantity * book.book.price
    order = Orders(
        books=book.book,
        user=request.user,
        quantity=book.quantity,
        total_price=total_price
    )
    order.save()
    for b in book.authorship.all():
        order.authorship.add(b)
    book.book.ordered += book.quantity
    book.book.number -= book.quantity
    if book.book.number == 0:
        book.book.available = False
    book.book.save()
    book.delete()
    return render(request, 'my_books/confirm_order.html')


class MyOrdersView(ListView):
    model = Orders
    context_object_name = 'orders'
    template_name = 'my_books/my_orders.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super(MyOrdersView, self).get_queryset()
        orders = queryset.filter(user=self.request.user)
        orders = orders.select_related('books').all()
        orders = orders.prefetch_related('authorship').all()
        return orders


def to_admin(request):
    pass
