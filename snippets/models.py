from django.db import models
from django.contrib.auth.models import User


# ======================= CATEGORY MODEL =======================

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


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
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publish_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    # Proper ForeignKey to Category
    category = models.ForeignKey(
    Category,
    on_delete=models.CASCADE,
    related_name="books"
    
)

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


# ======================= COMPLAINT MODEL =======================

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255)
    complaint_type = models.CharField(max_length=100, choices=[
        ('missing', 'Missing Book'),
        ('wrong_info', 'Wrong Information'),
        ('quality', 'Bad Quality'),
        ('other', 'Other Issue'),
    ])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_title
    

# ======================= READING HISTORY =======================

class ReadingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reading_history")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reading_history")
    progress = models.IntegerField(default=0)  # 0–100 %
    last_read = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.progress}%)"