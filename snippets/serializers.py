from rest_framework import serializers
from .models import Book, UserProfile, VisitorCount

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publish_date']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'firstname', 'lastname', 'email', 'phone', 'joined_date']


class VisitorCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorCount
        fields = ['id', 'count']