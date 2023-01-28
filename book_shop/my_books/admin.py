from django.contrib import admin
from django.db.models import QuerySet
from .models import *

# Register your models here.


class PriceFilter(admin.SimpleListFilter):
    title = 'Фильтр по цене'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return [
            ('<100', 'Низкая цена'),
            ('от 100 до 500', 'Средняя цена'),
            ('>=500', 'Высокая цена')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<100':
            return queryset.filter(price__lt=100)
        if self.value() == 'от 100 до 500':
            return queryset.filter(price__gte=100).filter(price__lt=500)
        if self.value() == '>=500':
            return queryset.filter(price__gte=500)
        return queryset


class OrderedFilter(admin.SimpleListFilter):
    title = 'Фильтр по заказам'
    parameter_name = 'ordered'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Меньше 10'),
            ('от 10 до 100', 'от 10 до 100'),
            ('>=100', 'От 100')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(ordered__lt=10)
        if self.value() == 'от 10 до 100':
            return queryset.filter(ordered__gte=10).filter(ordered__lt=100)
        if self.value() == '>=100':
            return queryset.filter(ordered__gte=100)
        return queryset


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'year', 'price', 'number', 'available', 'ordered']
    list_editable = ['price', 'number', 'available']
    list_filter = ['genre', 'year', PriceFilter, 'number', 'available', OrderedFilter]
    search_fields = ['title__startswith', 'authorship__name']
    filter_horizontal = ['authorship']
    list_per_page = 10
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name', 'country']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genres)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10
    search_fields = ['name__startswith']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['books', 'quantity', 'user', 'date', 'active']
    list_per_page = 10
    list_filter = ['books', 'user', 'active']
