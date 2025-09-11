
from django.contrib import admin
from .models import BlogPage, WebinarPage


@admin.register(BlogPage)
class BlogPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'live')
    list_filter = ('date', 'author', 'live')
    search_fields = ('title', 'intro', 'body')
    date_hierarchy = 'date'


@admin.register(WebinarPage)
class WebinarPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'status', 'live')
    list_filter = ('date', 'author', 'status', 'live')
    search_fields = ('title', 'intro', 'description')
    date_hierarchy = 'date'
