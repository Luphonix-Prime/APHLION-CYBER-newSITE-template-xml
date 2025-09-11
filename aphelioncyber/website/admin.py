from django.contrib import admin
from .models import ContactSubmission, UserSubscription, ServicePageContent, XMLContentImport

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'company')
    readonly_fields = ('created_at',)

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_type', 'status', 'last_active')
    list_filter = ('subscription_type', 'status', 'created_at')
    search_fields = ('user__username', 'user__email')

@admin.register(ServicePageContent)
class ServicePageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'xml_source_file', 'is_active', 'last_updated')
    list_filter = ('is_active', 'last_updated', 'created_at')
    search_fields = ('title', 'slug', 'description')
    readonly_fields = ('last_updated', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'is_active')
        }),
        ('Content Data', {
            'fields': ('content_data',),
            'classes': ('collapse',)
        }),
        ('Source & Timestamps', {
            'fields': ('xml_source_file', 'created_at', 'last_updated'),
            'classes': ('collapse',)
        }),
    )

@admin.register(XMLContentImport)
class XMLContentImportAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'processing_status', 'pages_created', 'pages_updated', 'processed_at')
    list_filter = ('processing_status', 'processed_at', 'created_at')
    search_fields = ('file_name', 'file_path')
    readonly_fields = ('created_at', 'processed_at')
    
    fieldsets = (
        ('File Information', {
            'fields': ('file_name', 'file_path')
        }),
        ('Processing Status', {
            'fields': ('processing_status', 'processed_at', 'error_message')
        }),
        ('Results', {
            'fields': ('pages_created', 'pages_updated', 'created_at')
        }),
    )