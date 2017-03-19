from django.contrib import admin
from blogs.models import Category, Blog, Post

admin.site.register(Category)
admin.site.register(Blog)


class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'publish_date']

admin.site.register(Post, PostAdmin)