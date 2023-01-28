from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from my_books.models import *
from django.contrib.auth.forms import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', )


class BooksSerializer(serializers.ModelSerializer):
    authorship = AuthorSerializer(many=True)
    genre = GenreSerializer(many=False)

    class Meta:
        model = Books
        fields = ('id', 'title', 'image', 'authorship', 'genre', 'year', 'description', 'price', 'number', 'available')


class BookTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('id', 'title', 'price')


class CartSerializer(serializers.ModelSerializer):
    #book = BookTitleSerializer(many=False)
    #authorship = AuthorSerializer(many=True)
    # из-за этого не получается создавать, изменять и удалять объекты

    class Meta:
        model = Cart
        fields = ('book', 'authorship', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    #books = BookTitleSerializer(many=False)
    #authorship = AuthorSerializer(many=True)

    class Meta:
        model = Orders
        fields = ('books', 'authorship', 'quantity', 'total_price')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        return user
