from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from my_admin.forms import UserInfoForm
from accounts.forms import RegisterUserForm


class Search(ListView):
    model = User
    paginate_by = 10
    template_name = 'users/admin_search_users.html'
    context_object_name = 'result'

    def get_queryset(self):
        queryset = super(Search, self).get_queryset()
        data = self.request.GET.get('q')
        result = queryset.filter(Q(username__icontains=data) | Q(first_name__icontains=data) | Q(last_name__icontains=data))
        return result

    def get_context_data(self, *args, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['data'] = self.request.GET.get('q')
        return context


class UserList(UserPassesTestMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/user_list.html'
    ordering = 'username'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserList, self).get_context_data()
        queryset = self.object_list
        context['quantity'] = len(queryset)
        return context


class UserDetail(UserPassesTestMixin, UpdateView):
    model = User
    context_object_name = 'user'
    form_class = UserInfoForm
    template_name = 'users/user.html'
    pk_url_kwarg = 'user_id'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        delete = self.request.POST.get('delete')
        save_and_add_new = self.request.POST.get('save_and_add_new')
        save_and_continue = self.request.POST.get('save_and_continue')
        save = self.request.POST.get('save')
        if save:
            return reverse_lazy('admin_users')
        elif delete:
            return reverse_lazy('admin_user_delete', kwargs={'user_id': self.object.id})
        elif save_and_add_new:
            return reverse_lazy('admin_add_user')
        elif save_and_continue:
            return reverse_lazy('admin_user', kwargs={'user_id': self.object.id})


class AddUserView(UserPassesTestMixin, CreateView):
    success_url = reverse_lazy('admin_users')
    form_class = RegisterUserForm
    template_name = 'users/add_user.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(AddUserView, self).get_context_data()
        context['new_user'] = RegisterUserForm
        return context

    def get_success_url(self):
        save_and_add_new = self.request.POST.get('save_and_add_new')
        save = self.request.POST.get('save')
        if save:
            return reverse_lazy('admin_users')
        elif save_and_add_new:
            return reverse_lazy('admin_add_user')


class DeleteUserView(UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete_user.html'
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('admin_users')
    context_object_name = 'user'

    def test_func(self):
        return self.request.user.is_staff
