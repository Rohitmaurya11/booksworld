from django.contrib import admin
from .models import Book, UserProfile, VisitorCount


# ======================= BOOK ADMIN =======================

class BookAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'author',
        'category',
        'publish_date',
        'created_by',
        'views',
        'downloads'
    )

    list_filter = ('category', 'publish_date', 'created_by')
    search_fields = ('title', 'author', 'category')

    fields = (
        'title',
        'author',
        'category',
        'publish_date',
        'description',
        'cover_image',
        'book_file',
        'created_by',
        'views',
        'downloads'
    )

    readonly_fields = ('views', 'downloads')


# ======================= USER PROFILE ADMIN =======================

class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('firstname', 'lastname', 'phone', 'role', 'joined_date', 'user')
    list_filter = ('role', 'joined_date')
    search_fields = ('firstname', 'lastname', 'phone', 'user__username')

    fields = (
        'user',
        'firstname',
        'lastname',
        'phone',
        'role',
        'joined_date'
    )

    readonly_fields = ('joined_date',)


# ======================= VISITOR COUNT ADMIN =======================

class VisitorCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'count')
    readonly_fields = ('count',)


# ======================= REGISTER MODELS =======================

admin.site.register(Book, BookAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(VisitorCount, VisitorCountAdmin)
