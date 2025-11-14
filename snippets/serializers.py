from rest_framework import serializers
from .models import Book, UserProfile

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publish_date']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'firstname', 'lastname', 'email', 'phone', 'joined_date']