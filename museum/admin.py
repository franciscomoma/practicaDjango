from django.contrib import admin
from museum.models import Picture, PictureFile, Size


class PictureFileInLine(admin.TabularInline):
    model = PictureFile


class PictureAdmin(admin.ModelAdmin):
    inlines = [PictureFileInLine, ]
    list_display = ['pk', 'name']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'method', 'width', 'height']


admin.site.register(Size, SizeAdmin)
admin.site.register(Picture, PictureAdmin)
