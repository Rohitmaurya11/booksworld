from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from django.db import models
from django.views.decorators.http import require_POST

from .models import Book, UserProfile, VisitorCount
from .serializers import BookSerializer, UserProfileSerializer
from .forms import UserRegisterForm


# -------------------- API VIEWSETS -------------------- #

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


# -------------------- HOME VIEW (USER PAGE) -------------------- #

def home(request):
    search = request.GET.get("search")
    category_filter = request.GET.get("category")

    books = Book.objects.all()

    # Search functionality
    if search:
        books = books.filter(
            models.Q(title__icontains=search) |
            models.Q(author__icontains=search) |
            models.Q(category__icontains=search)
        )

    # Category Filter
    if category_filter and category_filter != "All":
        books = books.filter(category=category_filter)

    categories = Book.CATEGORY_CHOICES

    return render(request, "index.html", {
        "books": books,
        "categories": categories
    })

def home(request):
    books = Book.objects.all()
    return render(request, "index.html", {"books": books})

# -------------------- REGISTER VIEW -------------------- #

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Assign to default "User" group
            try:
                default_group = Group.objects.get(name='User')
                user.groups.add(default_group)
            except Group.DoesNotExist:
                messages.warning(request, "Default User group not found.")

            # Send welcome email
            try:
                template = get_template('email.html')
                html = template.render({'username': username})
                msg = EmailMultiAlternatives(
                    'Welcome to Book World', html, 'your_email@gmail.com', [email]
                )
                msg.attach_alternative(html, 'text/html')
                msg.send()
            except:
                pass

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'signup.html', {'form': form})


# -------------------- LOGIN VIEW -------------------- #

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect_user_by_role(user)
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})


# -------------------- LOGOUT VIEW -------------------- #

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')


# -------------------- ROLE REDIRECTION -------------------- #

def redirect_user_by_role(user):
    if user.groups.filter(name='Admin').exists():
        return redirect('admin_dashboard')
    elif user.groups.filter(name='Manager').exists():
        return redirect('manager_dashboard')
    else:
        return redirect('index')


# -------------------- ADMIN DASHBOARD -------------------- #

@login_required
def admin_dashboard(request):
    search = request.GET.get("search")
    books = Book.objects.all()

    # Search in admin dashboard
    if search:
        books = books.filter(
            models.Q(title__icontains=search) |
            models.Q(author__icontains=search) |
            models.Q(category__icontains=search)
        )

    # Visitor Counter
    visitors = VisitorCount.objects.get(id=1).count

    return render(request, 'dashboard/admin_dashboard.html', {
        "books": books,
        "visitor_count": visitors
    })


# -------------------- MANAGER DASHBOARD -------------------- #

@login_required
def manager_dashboard(request):
    search = request.GET.get("search")

    # Manager sees only their books
    books = Book.objects.filter(created_by=request.user)

    if search:
        books = books.filter(
            models.Q(title__icontains=search) |
            models.Q(author__icontains=search) |
            models.Q(category__icontains=search)
        )

    categories = Book.CATEGORY_CHOICES

    return render(request, "dashboard/manager_dashboard.html", {
        "books": books,
        "categories": categories
    })


# -------------------- ADD BOOK (MANAGER) -------------------- #

@require_POST
@login_required
def add_book(request):
    Book.objects.create(
        title=request.POST.get("title"),
        author=request.POST.get("author"),
        publish_date=request.POST.get("publish_date"),
        description=request.POST.get("description"),
        category=request.POST.get("category"),
        cover_image=request.FILES.get("cover_image"),
        book_file=request.FILES.get("book_file"),
        created_by=request.user
    )

    messages.success(request, "Book added successfully!")
    return redirect('manager_dashboard')


# -------------------- EDIT BOOK -------------------- #

@login_required
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)

    book.title = request.POST.get("title")
    book.author = request.POST.get("author")
    book.publish_date = request.POST.get("publish_date")
    book.description = request.POST.get("description")
    book.save()

    return redirect("manager_dashboard")


# -------------------- DELETE BOOK -------------------- #

@login_required
def delete_book(request, book_id):
    Book.objects.get(id=book_id).delete()
    return redirect("manager_dashboard")


# -------------------- BOOK DETAIL PAGE -------------------- #

def book_detail(request, id):
    book = Book.objects.get(id=id)

    # Increase view count
    book.views += 1
    book.save()

    return render(request, "book_detail.html", {"book": book})


# -------------------- BOOK DOWNLOAD -------------------- #

def download_book(request, id):
    book = Book.objects.get(id=id)

    # Increase download count
    book.downloads += 1
    book.save()

    return redirect(book.book_file.url)
