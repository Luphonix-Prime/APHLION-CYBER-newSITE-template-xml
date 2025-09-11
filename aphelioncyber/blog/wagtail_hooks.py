
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import BlogPage, WebinarPage


class BlogPageAdmin(ModelAdmin):
    model = BlogPage
    menu_label = 'Blogs'
    menu_icon = 'doc-full-inverse'
    list_display = ('title', 'author', 'date', 'live')
    list_filter = ('author', 'date', 'live')
    search_fields = ('title', 'intro', 'body')


class WebinarPageAdmin(ModelAdmin):
    model = WebinarPage
    menu_label = 'Webinars'
    menu_icon = 'media'
    list_display = ('title', 'author', 'date', 'status', 'live')
    list_filter = ('author', 'date', 'status', 'live')
    search_fields = ('title', 'intro', 'description')


modeladmin_register(BlogPageAdmin)
modeladmin_register(WebinarPageAdmin)
