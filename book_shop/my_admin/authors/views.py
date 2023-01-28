from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView
from django.core.paginator import Paginator
from my_admin.accesses import super_access
from my_books.models import *
from my_admin.forms import AddAuthorForm


@super_access
def all_authors(request):
    authors = Author.objects.all()
    paginator = Paginator(authors, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'authors': authors,
        'total_quantity': len(authors),
        'paginator': paginator,
        'page_obj': page_obj
    }
    return render(request, 'authors/authors.html', context)


class AddAuthorViewCreate(UserPassesTestMixin, CreateView):
    form_class = AddAuthorForm
    template_name = 'authors/add_author.html'
    success_url = reverse_lazy('admin_authors')

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(AddAuthorViewCreate, self).get_context_data()
        context['new_author'] = AddAuthorForm
        return context

    def get_success_url(self):
        save_and_add_new = self.request.POST.get('save_and_add_new')
        save = self.request.POST.get('save')
        if save:
            return reverse_lazy('admin_authors')
        elif save_and_add_new:
            return reverse_lazy('admin_add_author')


class AuthorViewUpdate(UserPassesTestMixin, UpdateView):
    model = Author
    form_class = AddAuthorForm
    template_name = 'authors/author_detail.html'
    pk_url_kwarg = 'author_id'
    context_object_name = 'author'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        delete = self.request.POST.get('delete')
        save_and_add_new = self.request.POST.get('save_and_add_new')
        save_and_continue = self.request.POST.get('save_and_continue')
        save = self.request.POST.get('save')
        if save:
            return reverse_lazy('admin_authors')
        elif delete:
            return reverse_lazy('admin_author_delete', kwargs={'author_id': self.object.id})
        elif save_and_add_new:
            return reverse_lazy('admin_add_author')
        elif save_and_continue:
            return reverse_lazy('admin_author_detail', kwargs={'author_id': self.object.id})


class DeleteAuthorView(UserPassesTestMixin, DeleteView):
    model = Author
    template_name = 'authors/delete_author.html'
    pk_url_kwarg = 'author_id'
    success_url = reverse_lazy('admin_authors')
    context_object_name = 'author'

    def test_func(self):
        return self.request.user.is_staff
