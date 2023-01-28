from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView, ListView
from django.core.paginator import Paginator
from my_admin.accesses import super_access
from my_books.models import *
from my_admin.forms import AddBook


class Search(ListView):
    model = Books
    paginate_by = 2
    template_name = 'books/admin_search.html'
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


# @super_access
# def all_books(request):
#     books = Books.objects.all()
#     books = books.select_related('genre').all()
#     books = books.prefetch_related('authorship').all()
#     paginator = Paginator(books, per_page=2)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'books': books,
#         'total_quantity': len(books),
#         'paginator': paginator,
#         'page_obj': page_obj
#     }
#     return render(request, 'books/books.html', context)


class AllBooks(UserPassesTestMixin, ListView):
    model = Books
    template_name = 'books/books.html'
    context_object_name = 'books'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = super(AllBooks, self).get_queryset()
        queryset = queryset.prefetch_related('authorship').all()
        queryset = queryset.select_related('genre').all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AllBooks, self).get_context_data()
        context['total_quantity'] = len(self.object_list)
        return context


class AddBookViewCreate(UserPassesTestMixin, CreateView):
    form_class = AddBook
    template_name = 'books/add_book.html'
    success_url = reverse_lazy('admin_books')

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(AddBookViewCreate, self).get_context_data()
        context['new_book'] = AddBook
        return context

    def get_success_url(self):
        save_and_add_new = self.request.POST.get('save_and_add_new')
        save = self.request.POST.get('save')
        if save:
            return reverse_lazy('admin_books')
        elif save_and_add_new:
            return reverse_lazy('admin_add_book')


class BookViewUpdate(UserPassesTestMixin, UpdateView):
    model = Books
    form_class = AddBook
    template_name = 'books/book_detail.html'
    pk_url_kwarg = 'book_id'
    context_object_name = 'book'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        delete = self.request.POST.get('delete')
        save_and_add_new = self.request.POST.get('save_and_add_new')
        save_and_continue = self.request.POST.get('save_and_continue')
        save = self.request.POST.get('save')
        if save:
            return reverse_lazy('admin_books')
        elif delete:
            return reverse_lazy('admin_book_delete', kwargs={'book_id': self.object.id})
        elif save_and_add_new:
            return reverse_lazy('admin_add_book')
        elif save_and_continue:
            return reverse_lazy('admin_book_detail', kwargs={'book_id': self.object.id})


class DeleteBookView(UserPassesTestMixin, DeleteView):
    model = Books
    template_name = 'books/delete_book.html'
    pk_url_kwarg = 'book_id'
    success_url = reverse_lazy('admin_books')
    context_object_name = 'book'

    def test_func(self):
        return self.request.user.is_staff
