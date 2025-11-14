from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book, UserProfile


def setup_roles_and_permissions():
    # Get content types for both models
    book_ct = ContentType.objects.get_for_model(Book)
    userprofile_ct = ContentType.objects.get_for_model(UserProfile)

    # Define book permissions
    book_perms = {
        'add': Permission.objects.get(content_type=book_ct, codename='add_book'),
        'change': Permission.objects.get(content_type=book_ct, codename='change_book'),
        'delete': Permission.objects.get(content_type=book_ct, codename='delete_book'),
        'view': Permission.objects.get(content_type=book_ct, codename='view_book'),
    }

    # Define user profile permissions
    user_perms = {
        'add': Permission.objects.get(content_type=userprofile_ct, codename='add_userprofile'),
        'change': Permission.objects.get(content_type=userprofile_ct, codename='change_userprofile'),
        'delete': Permission.objects.get(content_type=userprofile_ct, codename='delete_userprofile'),
        'view': Permission.objects.get(content_type=userprofile_ct, codename='view_userprofile'),
    }

    # ---------- ADMIN GROUP ----------
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    admin_group.permissions.set([
        book_perms['add'], book_perms['change'], book_perms['delete'], book_perms['view'],
        user_perms['add'], user_perms['change'], user_perms['delete'], user_perms['view'],
    ])

    # ---------- MANAGER GROUP ----------
    manager_group, _ = Group.objects.get_or_create(name='Manager')
    manager_group.permissions.set([
        book_perms['add'], book_perms['change'], book_perms['view'],
        user_perms['view'],
    ])

    # ---------- USER GROUP ----------
    user_group, _ = Group.objects.get_or_create(name='User')
    user_group.permissions.set([
        book_perms['view'],
        user_perms['view']
    ])

    print('Roles and Permissions successfully created.')
