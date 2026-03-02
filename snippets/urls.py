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
    path('', views.login_view, name='root'),        
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
    path('admin_dashboard/add-book/', views.admin_add_book, name='admin_add_book'),
    path('admin_dashboard/add-book/admin_manage_books/', views.admin_manage_books, name='admin_manage_books'),
    path("admin_dashboard/users/change-role/<int:user_id>/",views.change_user_role,name="change_user_role"),    
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    
    
    # -------------------- BOOK CRUD (ROLE BASED) -------------------- #
    path('book/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('book/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('add_book/', views.add_book, name='add_book'),
    path('my_books/', views.my_books, name='my_books'),
    path('admin_dashboard/categories/', views.admin_manage_category,name='admin_manage_category'),
    path('admin_dashboard/categories/delete/<int:category_id>/',views.delete_category,name='delete_category'),

    # -------------------- MANAGER DASHBOARD -------------------- #
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),

    # -------------------- ADMIN DASHBOARDS -------------------- #
    # path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path("admin_dashboard/users/", views.manage_users, name="manage_users"),
    # path("admin_dashboard/users/make-admin/<int:user_id>/", views.make_admin, name="make_admin"),
    # path("admin_dashboard/users/delete/<int:user_id>/", views.delete_user, name="delete_user"),
    # path("admin_dashboard/analytics/", views.analytics, name="analytics"),
    # path('admin/add-book/', views.admin_add_book, name='admin_add_book'),



    # # -------------------- MANAGER DASHBOARDS -------------------- #
    # path('admin_dashboard/book/edit/<int:pk>/',views.edit_book,name='edit_book'),
    # path('admin_dashboard/book/delete/<int:pk>/',views.edit_book,name='delete_book'),
    # path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),


    # # -------------------- BOOK CRUD (MANAGER ONLY) -------------------- #
    # path('add_book/', views.add_book, name='add_book'),
    # path('my_books/', views.my_books, name='my_books'),
    # path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    # path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),


    # # -------------------- BOOK DETAIL, READ & DOWNLOAD -------------------- #
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('book/read/<int:id>/', views.read_book, name='read_book'),
    path('book/download/<int:id>/', views.download_book, name='download_book'),

    path('complain/', views.complain_view, name='complain'),
    path('dashboard/complaints/', views.admin_complaints, name='admin_complaints'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
