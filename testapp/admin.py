from django.contrib import admin

# Register your models here.
from .models import Book, UserData

admin.site.register(Book)
admin.site.register(UserData)