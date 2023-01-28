from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView

from .accesses import super_access
from my_books.models import *


@super_access
def index(request):
    return render(request, 'my_admin/index.html')


# @super_access
# def all_orders(request):
#     orders = Orders.objects.all()
#     orders = orders.select_related('user').all()
#     orders = orders.select_related('books').all()
#     orders = orders.prefetch_related('authorship').all()
#     paginator = Paginator(orders, per_page=10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'orders': orders,
#         'total_quantity': len(orders),
#         'paginator': paginator,
#         'page_obj': page_obj
#     }
#     return render(request, 'my_admin/orders.html', context)


class AllOrdersView(UserPassesTestMixin, ListView):
    model = Orders
    template_name = 'my_admin/orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = super(AllOrdersView, self).get_queryset()
        queryset = queryset.select_related('books').all()
        queryset = queryset.prefetch_related('authorship').all()
        queryset = queryset.select_related('user').all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AllOrdersView, self).get_context_data()
        orders = self.get_queryset()
        context['total_quantity'] = len(orders)
        return context


@super_access
def order_detail(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    return render(request, 'my_admin/confirm_order.html', {'order': order})


@super_access
def complete_order(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    order.active = True
    order.save()
    return HttpResponseRedirect(reverse('admin_orders'))
