
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from wagtail.models import Site, Page
from aphelioncyber.blog.models import BlogIndexPage, WebinarIndexPage


class Command(BaseCommand):
    help = 'Set up Wagtail CMS with initial blog and webinar pages'

    def handle(self, *args, **options):
        # Create user groups with permissions
        admin_group, created = Group.objects.get_or_create(name='Blog Administrators')
        moderator_group, created = Group.objects.get_or_create(name='Content Moderators')
        author_group, created = Group.objects.get_or_create(name='Content Authors')

        # Assign permissions
        blog_permissions = Permission.objects.filter(
            content_type__app_label='blog'
        )
        
        admin_group.permissions.set(blog_permissions)
        moderator_group.permissions.set(blog_permissions.filter(
            codename__in=['change_blogpage', 'change_webinarpage', 'view_blogpage', 'view_webinarpage']
        ))
        author_group.permissions.set(blog_permissions.filter(
            codename__in=['add_blogpage', 'add_webinarpage', 'change_blogpage', 'change_webinarpage']
        ))

        # Get or create root page
        root_page = Page.objects.filter(depth=1).first()
        if not root_page:
            self.stdout.write("No root page found. Please run wagtail migrations first.")
            return

        # Create blog index page
        blog_index, created = BlogIndexPage.objects.get_or_create(
            title='Blog',
            defaults={
                'intro': 'Stay up-to-date with the latest cybersecurity insights and best practices.',
                'slug': 'blog',
            }
        )
        if created:
            root_page.add_child(instance=blog_index)
            self.stdout.write(f"Created blog index page: {blog_index.title}")

        # Create webinar index page
        webinar_index, created = WebinarIndexPage.objects.get_or_create(
            title='Webinars',
            defaults={
                'intro': 'Join our expert-led webinars and events to enhance your cybersecurity knowledge.',
                'slug': 'webinars',
            }
        )
        if created:
            root_page.add_child(instance=webinar_index)
            self.stdout.write(f"Created webinar index page: {webinar_index.title}")

        # Update site settings
        site = Site.objects.get(is_default_site=True)
        if site.root_page != root_page:
            site.root_page = root_page
            site.save()

        self.stdout.write(
            self.style.SUCCESS('Successfully set up Wagtail CMS with blog and webinar functionality!')
        )
        self.stdout.write('Access the Wagtail admin at /cms/ to start creating content.')
