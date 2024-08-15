from django.contrib import admin
from add_books.models import AddBook

class AddBookAdmin(admin.ModelAdmin):
    list_display = ('title','author','price','image')
admin.site.register(AddBook,AddBookAdmin)
