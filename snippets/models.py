from django.db import models
from django.contrib.auth.models import User


# ======================= USER PROFILE MODEL =======================

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    joined_date = models.DateTimeField(auto_now_add=True)

    role = models.CharField(
        max_length=20,
        choices=[
            ('Admin', 'Admin'),
            ('Manager', 'Manager'),
            ('User', 'User'),
        ],
        default='User'
    )

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.role})"


# ======================= BOOK MODEL =======================

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Self-help', 'Self-help'),
        ('Business', 'Business'),
        ('Spiritual', 'Spiritual'),
        ('Programming', 'Programming'),
        ('Motivation', 'Motivation'),
        ('Biography', 'Biography'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publish_date = models.DateTimeField(null=True, auto_now=False, auto_now_add=False)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')

    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    book_file = models.FileField(upload_to='book_files/', null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # Analytics
    views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


# ======================= VISITOR COUNTER =======================

class VisitorCount(models.Model):
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Visitors: {self.count}"
