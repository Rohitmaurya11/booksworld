from rest_framework import viewsets
from django.shortcuts import render, redirect,get_object_or_404
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.db import models

from .models import Book, UserProfile, VisitorCount, Complaint
from .serializers import BookSerializer, UserProfileSerializer
from .forms import UserRegisterForm


# =======================================================================
#                               API VIEWSETS
# =======================================================================

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


# =======================================================================
#                               HOME 
# =======================================================================

def home(request):

    # FIX: redirect guests to login (do NOT render login page here)
    if not request.user.is_authenticated:
        return redirect("signup")

    search = request.GET.get("search")
    category_filter = request.GET.get("category")

    books = Book.objects.all()

    if search:
        books = books.filter(
            models.Q(title__icontains=search) |
            models.Q(author__icontains=search)
        )

    if category_filter and category_filter != "All":
        books = books.filter(category=category_filter)

    categories = Book.CATEGORY_CHOICES

    return render(request, "index.html", {
        "books": books,
        "categories": categories
    })

# =======================================================================
#                               CATEGORIES PAGE
# =======================================================================
def category(request):
    return render(request,"category.html")



# =======================================================================
#                               ABOUT PAGE
# =======================================================================

def about(request):
    return render(request, "about.html")

# =======================================================================
#                               CONTACT PAGE
# =======================================================================
def contact(request):
    return render(request,"contact.html")


# =======================================================================
#                               REGISTER
# =======================================================================

def register(request):

    # FIX: Allow signup page even when logged in
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Add user to default group
            try:
                group = Group.objects.get(name="User")
                user.groups.add(group)
            except Group.DoesNotExist:
                messages.warning(request, "User group not found.")

            # Send welcome email (optional)
            try:
                template = get_template('email.html')
                html = template.render({'username': username})

                msg = EmailMultiAlternatives(
                    'Welcome to Book World',
                    html,
                    'your_email@gmail.com',
                    [email]
                )
                msg.attach_alternative(html, 'text/html')
                msg.send()

            except Exception:
                pass

            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")

    else:
        form = UserRegisterForm()

    return render(request, 'signup.html', {"form": form})


# =======================================================================
#                               LOGIN
# =======================================================================

def login_view(request):

    # FIX: Allow authenticated users to visit /signup/
    if request.user.is_authenticated and request.path != "/signup.html/":
        return redirect_user_by_role(request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect_user_by_role(user)
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})


# =======================================================================
#                               LOGOUT
# =======================================================================

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


# =======================================================================
#                          REDIRECT BY ROLE
# =======================================================================

def redirect_user_by_role(user):

    if user.groups.filter(name="Admin").exists():
        return redirect("admin_dashboard")

    if user.groups.filter(name="Manager").exists():
        return redirect("manager_dashboard")

    return redirect("index")


# =======================================================================
#                          ADMIN DASHBOARD
# =======================================================================

@login_required
def admin_dashboard(request):
    search = request.GET.get("search")

    books = Book.objects.all().order_by('-id')

    if search:
        books = books.filter(
            models.Q(title__icontains=search) |
            models.Q(author__icontains=search)
        )

    visitor_count = VisitorCount.objects.get(id=1).count

    return render(request, "dashboard/admin_dashboard.html", {
        "books": books,
        "visitor_count": visitor_count
    })

# =======================================================================
#                          MANAGE USERS 
# =======================================================================

def manage_users(request):
    if not request.user.is_staff:
        return redirect("index")

    users = User.objects.all().order_by("-date_joined")
    return render(request, "dashboard/manage_users.html", {"users": users})

def make_admin(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_staff = True
    user.save()
    messages.success(request, f"{user.username} is now Admin")
    return redirect("manage_users")


def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect("manage_users")

# ==================== USER MANAGEMENT ======================

def manage_users(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("index")

    users = User.objects.all().order_by("-date_joined")
    return render(request, "dashboard/manage_users.html", {"users": users})


def make_admin(request, user_id):
    if not request.user.is_staff:
        return redirect("index")

    user = get_object_or_404(User, id=user_id)
    user.is_staff = True
    user.save()

    messages.success(request, f"{user.username} is now an Admin.")
    return redirect("manage_users")


def delete_user(request, user_id):
    if not request.user.is_staff:
        return redirect("index")

    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect("manage_users")

    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect("manage_users")












# ==================== BOOK EDIT / DELETE ======================

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.category = request.POST.get("category")
        if "cover_image" in request.FILES:
            book.cover_image = request.FILES["cover_image"]
        book.save()

        messages.success(request, "Book updated successfully!")
        return redirect("admin_dashboard")

    return render(request, "dashboard/edit_book.html", {"book": book})


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    messages.success(request, "Book deleted successfully!")
    return redirect("admin_dashboard")






# =======================================================================
#                         MANAGER DASHBOARD
# =======================================================================

@login_required
def manager_dashboard(request):
    search = request.GET.get("search")

    books = Book.objects.filter(created_by=request.user)

    if search:
        books = books.filter(
            models.Q(title__icontains=search) |
            models.Q(author__icontains=search)
        )

    categories = Book.CATEGORY_CHOICES

    return render(request, "dashboard/manager_dashboard.html", {
        "books": books,
        "categories": categories,
        "total_books": books.count(),
        "recent_books": books.order_by("-id")[:5].count()
    })


# =======================================================================
#                           LIST MY BOOKS
# =======================================================================

@login_required
def my_books(request):
    books = Book.objects.filter(created_by=request.user)
    return render(request, "dashboard/my_books.html", {"books": books})


# =======================================================================
#                          ADD BOOK
# =======================================================================

@login_required
def add_book(request):
    categories = Book.CATEGORY_CHOICES

    if request.method == "POST":
        Book.objects.create(
            title=request.POST.get("title"),
            author=request.POST.get("author"),
            publish_date=request.POST.get("publish_date"),
            category=request.POST.get("category"),
            description=request.POST.get("description"),
            cover_image=request.FILES.get("cover_image"),
            book_file=request.FILES.get("book_file"),
            created_by=request.user
        )

        messages.success(request, "Book added successfully!")
        return redirect("my_books")

    return render(request, "dashboard/add_book.html", {"categories": categories})


# =======================================================================
#                          EDIT BOOK
# =======================================================================

@login_required
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)

    if book.created_by != request.user:
        messages.error(request, "You cannot edit someone else's book!")
        return redirect("my_books")

    categories = Book.CATEGORY_CHOICES

    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.category = request.POST.get("category")
        book.description = request.POST.get("description")

        if request.FILES.get("cover_image"):
            book.cover_image = request.FILES.get("cover_image")

        if request.FILES.get("book_file"):
            book.book_file = request.FILES.get("book_file")

        book.save()
        messages.success(request, "Book updated successfully!")
        return redirect("my_books")

    return render(request, "dashboard/edit_book.html", {
        "book": book,
        "categories": categories
    })


# =======================================================================
#                          DELETE BOOK
# =======================================================================

@login_required
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)

    if book.created_by != request.user:
        messages.error(request, "You cannot delete someone else's book!")
        return redirect("my_books")

    book.delete()
    messages.success(request, "Book deleted successfully!")
    return redirect("my_books")


# =======================================================================
#                          BOOK DETAIL
# =======================================================================

@login_required
def book_detail(request, id):
    book = Book.objects.get(id=id)
    book.views += 1
    book.save()

    return render(request, "book_detail.html", {"book": book})


# =======================================================================
#                       READ BOOK (PDF VIEWER PAGE)
# =======================================================================

@login_required
def read_book(request, id):
    book = Book.objects.get(id=id)
    book.views += 1
    book.save()

    return render(request, "read_book.html", {"book": book})


# =======================================================================
#                       DOWNLOAD BOOK
# =======================================================================

@login_required
def download_book(request, id):
    book = Book.objects.get(id=id)
    book.downloads += 1
    book.save()

    return redirect(book.book_file.url)


# =======================================================================
#                       BOOK CATEGORIES
# =======================================================================
def book_categories(request):

    # search functionality
    q = request.GET.get('q', '').strip()

    # get all category names from BOOK choices
    all_categories = [c[0] for c in Book.CATEGORY_CHOICES]

    # if search entered → filter categories
    if q:
        categories = [c for c in all_categories if q.lower() in c.lower()]
    else:
        categories = all_categories

    # fetch all books (template filters them)
    books = Book.objects.all()

    return render(request, 'category.html', {
        'categories': categories,
        'books': books,
        'query': q,
    })

def book_categories(request):
    books = Book.objects.all()
    categories = books.values_list("category", flat=True).distinct()

    category_data = {}

    for cat in categories:
        category_data[cat] = books.filter(category=cat)

    return render(request, "category.html", {
        "category_data": category_data,
    })

@login_required
def complain_view(request):
    if request.method == "POST":
        Complaint.objects.create(
            user=request.user,
            book_title=request.POST.get('book_title'),
            complaint_type=request.POST.get('complaint_type'),
            message=request.POST.get('message')
        )
        messages.success(request, "Complaint submitted successfully!")
        return redirect('index')

    return render(request, 'complain.html')


# Only admin/staff can view complaints
@user_passes_test(lambda u: u.is_staff)
def admin_complaints(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, "dashboard/admin_complaints.html", {"complaints": complaints})



# =======================================================================
#                       ANALAYTICS PAGE
# =======================================================================



def analytics(request):

    # --- TOP COUNTS ---
    total_books = Book.objects.count()
    total_users = User.objects.count()
    total_categories = Book.objects.values('category').distinct().count()
    total_complaints = Complaint.objects.count()

    # --- CATEGORY WISE BOOKS ---
    category_data = Book.objects.values('category').annotate(count=models.Count('id'))
    categories = [item['category'] for item in category_data]
    category_counts = [item['count'] for item in category_data]

    # --- USER STATUS PIE CHART ---
    active_users = User.objects.filter(is_active=True).count()
    inactive_users = User.objects.filter(is_active=False).count()

    # --- LATEST BOOKS ---
    latest_books = Book.objects.order_by('-id')[:5]

    # --- LATEST COMPLAINTS ---
    latest_complaints = Complaint.objects.order_by('-id')[:5]

    return render(request, "dashboard/analytics.html", {
        "total_books": total_books,
        "total_users": total_users,
        "total_categories": total_categories,
        "total_complaints": total_complaints,

        "categories": categories,
        "category_counts": category_counts,

        "active_users": active_users,
        "inactive_users": inactive_users,

        "latest_books": latest_books,
        "latest_complaints": latest_complaints,
    })