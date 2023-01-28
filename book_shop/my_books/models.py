from django.conf import settings
from django.db import models
from django.urls import reverse


class Author(models.Model):
    """ Авторы """
    name = models.CharField(max_length=255, verbose_name='Автор')
    country = models.CharField(max_length=255, blank=True, null=True, verbose_name='Страна')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'author_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['name']


class Genres(models.Model):
    """ Жанры """
    name = models.CharField(max_length=255, verbose_name='Жанр')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('genre_detail', kwargs={'genre_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Books(models.Model):
    """ Книги """
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='titles', blank=True, null=True, verbose_name='Обложка')
    authorship = models.ManyToManyField(Author, blank=True, verbose_name='Соавторство', related_name='authorship')
    genre = models.ForeignKey(Genres, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Жанр')
    year = models.PositiveIntegerField(blank=True, null=True, verbose_name='Год')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Цена')
    number = models.PositiveIntegerField(default=1, verbose_name='Количество')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    ordered = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='Заказы')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'book_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'
        ordering = ['title']


class Cart(models.Model):
    book = models.ForeignKey(Books, null=True, on_delete=models.CASCADE, verbose_name='Книга')
    authorship = models.ManyToManyField(Author, blank=True, verbose_name='Соавторство')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                             verbose_name='Пользователь')
    create_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.book

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-create_date']


class Orders(models.Model):
    books = models.ForeignKey(Books, null=True, on_delete=models.SET_NULL, verbose_name='Книги')
    authorship = models.ManyToManyField(Author, blank=True, verbose_name='Соавторство')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                             verbose_name='Пользователь')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Общая цена')
    date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата заказа')
    active = models.BooleanField(default=False, verbose_name='Завершённый')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-date']
