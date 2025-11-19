from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import BookViewSet, UserProfileViewSet
from snippets import views as user_view


# -------------------- DRF ROUTER -------------------- #
router = DefaultRouter()
router.register(r'books', BookViewSet, basename="books")
router.register(r'userprofiles', UserProfileViewSet, basename="userprofiles")


# -------------------- URL PATTERNS -------------------- #

urlpatterns = [

    # -------------------- API ROUTES -------------------- #
    path('api/', include(router.urls)),

    # -------------------- AUTH ROUTES -------------------- #
    path('', views.login_view, name='signup'),        # Default page
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', user_view.register, name='signup'),

    # -------------------- PUBLIC ROUTES -------------------- #
    path('home/', views.home, name='index'),
    path('about/', views.about, name='about'),
    path('contact/',views.contact,name='contact'),
    path('category/',views.book_categories,name='category'),
    path('category/', views.book_categories, name='category'),


    # -------------------- ADMIN DASHBOARDS -------------------- #
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path("admin_dashboard/users/", views.manage_users, name="manage_users"),
    path("admin_dashboard/users/make-admin/<int:user_id>/", views.make_admin, name="make_admin"),
    path("admin_dashboard/users/delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path("admin_dashboard/analytics/", views.analytics, name="analytics"),



    # -------------------- MANAGER DASHBOARDS -------------------- #
    path('admin_dashboard/book/edit/<int:pk>/',views.edit_book,name='edit_book'),
    path('admin_dashboard/book/delete/<int:pk>/',views.edit_book,name='delete_book'),



    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),

    # -------------------- BOOK CRUD (MANAGER ONLY) -------------------- #
    path('add_book/', views.add_book, name='add_book'),
    path('my_books/', views.my_books, name='my_books'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),

    # -------------------- BOOK DETAIL, READ & DOWNLOAD -------------------- #
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('book/read/<int:id>/', views.read_book, name='read_book'),
    path('book/download/<int:id>/', views.download_book, name='download_book'),

    path('complain/', views.complain_view, name='complain'),
    path('dashboard/complaints/', views.admin_complaints, name='admin_complaints'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
