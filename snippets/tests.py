from django.test import TestCase

# Create your tests here.




# from snippets.models import Category, Book

# # Create categories matching old data
# for name in ['Fiction','Self-help','Business','Spiritual','Health','Science','History','Computer Science','Artifical Intelligence','Cloud Computing','Programming','Motivation','Biography','Other']:
#     Category.objects.get_or_create(name=name)

# # Assign categories properly
# for book in Book.objects.all():
#     cat = Category.objects.filter(name=book.category_id).first()
#     if cat:
#         book.category = cat
#         book.save()