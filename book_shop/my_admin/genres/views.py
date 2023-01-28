from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView
from django.core.paginator import Paginator
from my_admin.accesses import super_access
from my_books.models import *
from my_admin.forms import AddGenreForm


@super_access
def all_genres(request):
    genres = Genres.objects.all()
    paginator = Paginator(genres, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'genres': genres,
        'total_quantity': len(genres),
        'paginator': paginator,
        'page_obj': page_obj
    }
    return render(request, 'genres/genres.html', context)


class AddGenreViewCreate(UserPassesTestMixin, CreateView):
    form_class = AddGenreForm
    template_name = 'genres/add_genre.html'
    success_url = reverse_lazy('admin_genres')

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(AddGenreViewCreate, self).get_context_data()
        context['new_genre'] = AddGenreForm
        return context

    def get_success_url(self):
        save_and_add_new = self.request.POST.get('save_and_add_new')
        save = self.request.POST.get('save')
        if save:
            return reverse_lazy('admin_genres')
        elif save_and_add_new:
            return reverse_lazy('admin_add_genre')


class GenreViewUpdate(UserPassesTestMixin, UpdateView):
    model = Genres
    form_class = AddGenreForm
    template_name = 'genres/genre_detail.html'
    pk_url_kwarg = 'genre_id'
    context_object_name = 'genre'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        delete = self.request.POST.get('delete')
        save_and_add_new = self.request.POST.get('save_and_add_new')
        save_and_continue = self.request.POST.get('save_and_continue')
        save = self.request.POST.get('save')
        if save:
            return reverse_lazy('admin_genres')
        elif delete:
            return reverse_lazy('admin_genre_delete', kwargs={'genre_id': self.object.id})
        elif save_and_add_new:
            return reverse_lazy('admin_add_genre')
        elif save_and_continue:
            return reverse_lazy('admin_genre_detail', kwargs={'genre_id': self.object.id})


class DeleteGenreView(UserPassesTestMixin, DeleteView):
    model = Genres
    template_name = 'genres/delete_genre.html'
    pk_url_kwarg = 'genre_id'
    success_url = reverse_lazy('admin_genres')
    context_object_name = 'genre'

    def test_func(self):
        return self.request.user.is_staff
