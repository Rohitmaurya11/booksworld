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

    # API ROUTES
    path('api/', include(router.urls)),

    # AUTH
    path('', views.login_view, name='login'),   # Default route
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', user_view.register, name='register'),

    # HOME PAGE
    path('home/', views.home, name='index'),

    # DASHBOARDS
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),

    # BOOK CRUD
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),

    # BOOK DETAIL + DOWNLOAD
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('book/download/<int:id>/', views.download_book, name='download_book'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
