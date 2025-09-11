# Replit.md

## Overview

This repository contains the Aphelion Cyber Security platform, a comprehensive Django-based cybersecurity solution that provides managed security services, cyber defense capabilities, and compliance tools. The platform includes a CMS-powered blog, security assessment tools, and a client-facing website with extensive cybersecurity service offerings.

The application is built to serve as both a marketing website and a functional security platform, featuring services like vulnerability assessment, penetration testing, compliance management, and security operations center capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Django 5.2.1 with Python
- **CMS Integration**: Wagtail CMS for content management, enabling non-technical users to manage blog posts, webinars, and website content
- **Authentication**: Django's built-in authentication system with custom user management
- **Database**: Django ORM with SQLite for development (configurable for production databases)
- **Form Handling**: Django Crispy Forms with Tailwind styling for consistent form presentation

### Frontend Architecture
- **Styling**: Tailwind CSS via CDN for responsive design and rapid development
- **UI Components**: Custom CSS components with cybersecurity-themed styling (dark backgrounds, purple/blue color scheme)
- **Typography**: Inter font family for modern, professional appearance
- **Icons**: Remix Icon library for consistent iconography
- **Interactive Elements**: Custom JavaScript for dropdown menus, form handling, and dynamic content

### Application Structure
- **Core Apps**:
  - `website`: Main application handling static pages, contact forms, and service pages
  - `blog`: Wagtail-powered blog system with BlogPage and WebinarPage models
- **URL Routing**: Hierarchical URL structure with Wagtail handling CMS routes and Django handling application routes
- **Template System**: Base template with block inheritance, shared across all pages

### Data Models
- **Contact Management**: ContactSubmission model for handling contact form data
- **User Subscriptions**: UserSubscription model for tracking user engagement and subscription status
- **Content Management**: Wagtail models for blog posts and webinars with rich text fields, images, and metadata

### Security Features
- **CSRF Protection**: Django CSRF middleware enabled
- **Input Validation**: Form validation through Django forms and Crispy Forms
- **Static File Security**: Proper static file handling with debug-aware serving
- **Secret Management**: Environment variable support for sensitive configuration

### Development Configuration
- **Debug Mode**: Enabled for development with detailed error pages
- **Static Files**: Django static files handling with separate CSS and JS organization
- **Media Handling**: Wagtail image and document management
- **Admin Interface**: Django admin and Wagtail admin for content management

## External Dependencies

### Core Dependencies
- **Django**: Web framework providing ORM, templating, and admin functionality
- **Wagtail**: Headless CMS providing content management capabilities for blogs and pages
- **wagtail-modeladmin**: Admin interface extensions for better content management

### Frontend Dependencies
- **Tailwind CSS**: Utility-first CSS framework delivered via CDN
- **Google Fonts**: Inter font family for typography
- **Remix Icon**: Icon library for UI elements

### Form and UI Dependencies
- **django-crispy-forms**: Enhanced form rendering and validation
- **crispy-tailwind**: Tailwind CSS integration for Crispy Forms

### Document Generation
- **ReportLab**: PDF generation capabilities for security reports and documentation
- **Pillow**: Image processing library for handling uploaded images and graphics

### Production Dependencies
- **Gunicorn**: WSGI HTTP server for production deployment
- **ASGI/WSGI Support**: Both ASGI and WSGI configurations for deployment flexibility

### Development Tools
- **Django Debug Mode**: Comprehensive error reporting and debugging tools
- **Static File Serving**: Development server capabilities for CSS/JS/image serving

The application follows Django best practices with clear separation of concerns, modular app structure, and proper configuration management for different environments.