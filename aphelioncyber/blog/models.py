
from django.db import models
from django.contrib.auth.models import User
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail.images.models import Image


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context


class BlogPage(Page):
    date = models.DateTimeField("Post date")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts')
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('author'),
            FieldPanel('tags'),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        FieldPanel('featured_image'),
    ]


class WebinarIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        context = super().get_context(request)
        webinarpages = self.get_children().live().order_by('-first_published_at')
        context['webinarpages'] = webinarpages
        return context


class WebinarPage(Page):
    EVENT_STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('live', 'Live Now'),
        ('completed', 'Completed'),
    ]

    date = models.DateTimeField("Event date")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='webinar_posts')
    intro = models.CharField(max_length=250)
    description = RichTextField(blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    registration_link = models.URLField(blank=True, help_text="Link for webinar registration")
    status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES, default='upcoming')
    duration_minutes = models.PositiveIntegerField(default=60, help_text="Duration in minutes")
    max_attendees = models.PositiveIntegerField(blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('author'),
            FieldPanel('status'),
            FieldPanel('duration_minutes'),
            FieldPanel('max_attendees'),
            FieldPanel('tags'),
        ], heading="Webinar information"),
        FieldPanel('intro'),
        FieldPanel('description', classname="full"),
        FieldPanel('featured_image'),
        FieldPanel('registration_link'),
    ]
