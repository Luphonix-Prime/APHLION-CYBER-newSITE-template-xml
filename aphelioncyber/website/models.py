from django.db import models
import json

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.company}"


class UserSubscription(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    last_active = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type}"


class ServicePageContent(models.Model):
    """Model to store dynamic content for service pages from XML"""
    slug = models.SlugField(max_length=200, unique=True, help_text="URL slug for the service page")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content_data = models.JSONField(default=dict, help_text="Structured content data from XML")
    xml_source_file = models.CharField(max_length=300, blank=True, help_text="Source XML file name")
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Service Page Content"
        verbose_name_plural = "Service Page Contents"
        ordering = ['title']
    
    def __str__(self):
        return f"{self.title} ({self.slug})"
    
    def get_sections(self):
        """Get structured sections from content_data"""
        return self.content_data.get('sections', [])
    
    def get_benefits(self):
        """Get benefits list from content_data"""
        return self.content_data.get('benefits', [])
    
    def get_solutions(self):
        """Get solutions list from content_data"""
        return self.content_data.get('solutions', [])
    
    def get_process_steps(self):
        """Get process steps from content_data"""
        return self.content_data.get('process_steps', [])
    
    def get_statistics(self):
        """Get statistics from content_data"""
        return self.content_data.get('statistics', [])


class XMLContentImport(models.Model):
    """Track XML file imports and processing status"""
    file_name = models.CharField(max_length=300)
    file_path = models.CharField(max_length=500)
    processing_status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    pages_created = models.PositiveIntegerField(default=0)
    pages_updated = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "XML Content Import"
        verbose_name_plural = "XML Content Imports"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.file_name} - {self.processing_status}"