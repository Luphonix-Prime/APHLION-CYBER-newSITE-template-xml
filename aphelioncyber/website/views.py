from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import UserSubscription, ServicePageContent
from django.http import HttpResponse
import csv
from reportlab.pdfgen import canvas
from io import BytesIO

def home(request):
    return render(request, 'website/home.html')

def platform(request):
    return render(request, 'website/platform.html')

def managed_security(request):
    return render(request, 'website/managed_security.html')

def cyber_defense(request):
    return render(request, 'website/cyber_defense.html')

def cybersecurity_operations(request):
    return render(request, 'website/cybersecurity_operations.html')

def training_awareness(request):
    return render(request, 'website/training_awareness.html')

def pricing(request):
    return render(request, 'website/pricing.html')

def resources(request):
    from aphelioncyber.blog.models import BlogPage, WebinarPage
    
    # Get latest blogs and webinars
    latest_blogs = BlogPage.objects.live().order_by('-date')[:6]
    latest_webinars = WebinarPage.objects.live().order_by('-date')[:6]
    
    context = {
        'latest_blogs': latest_blogs,
        'latest_webinars': latest_webinars,
    }
    return render(request, 'website/resources.html', context)

def company(request):
    return render(request, 'website/company.html')

# Remove or comment out the existing login view
# def login(request):
#     return render(request, 'website/login.html')

# Add these imports at the top
from django.contrib.auth.views import LoginView

# Add the custom login view
class CustomLoginView(LoginView):
    template_name = 'website/login.html'
    redirect_authenticated_user = True

def forgot_password(request):
    if request.method == 'POST':
        # Add your password reset logic here
        # For example, send a reset email
        messages.success(request, 'Password reset instructions have been sent to your email.')
        return redirect('login')
    return render(request, 'website/forgot_password.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. We will get back to you soon!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'website/contact.html', {'form': form})

def signup(request):
    return render(request, 'website/signup.html')

def security(request):
    return render(request, 'website/security.html')

def compliance(request):
    return render(request, 'website/compliance.html')

def addons(request):
    return render(request, 'website/addons.html')



# Managed Security Services subsections
def incident_response(request):
    return render(request, 'website/incident_response.html')

def deep_web_monitoring(request):
    # Try to get dynamic content from database
    try:
        page_content = ServicePageContent.objects.get(slug='deep-web-monitoring', is_active=True)
        context = {
            'page_content': page_content,
            'sections': page_content.get_sections(),
            'benefits': page_content.get_benefits(),
            'solutions': page_content.get_solutions(),
            'process_steps': page_content.get_process_steps(),
            'statistics': page_content.get_statistics(),
        }
    except ServicePageContent.DoesNotExist:
        # Fallback to static template if no dynamic content
        context = {}
    
    return render(request, 'website/deep_web_monitoring.html', context)

def security_operations_center(request):
    return render(request, 'website/security_operations_center.html')

def identity_access_management(request):
    return render(request, 'website/identity_access_management.html')

def third_party_risk_management(request):
    return render(request, 'website/third_party_risk_management.html')

# Cyber Defense subsections
def vapt(request):
    return render(request, 'website/vapt.html')

def website_application_security(request):
    return render(request, 'website/website_application_security.html')

def mobile_application_security(request):
    return render(request, 'website/mobile_application_security.html')

def api_security_assessment(request):
    return render(request, 'website/api_security_assessment.html')

def wireless_device_security(request):
    return render(request, 'website/wireless_device_security.html')

def cloud_security_testing(request):
    return render(request, 'website/cloud_security_testing.html')

def source_code_review(request):
    return render(request, 'website/source_code_review.html')

def ot_iot_security(request):
    return render(request, 'website/ot_iot_security.html')

# Governance, Risk & Compliance subsections
def iso_27001(request):
    return render(request, 'website/iso_27001.html')

def hipaa(request):
    return render(request, 'website/hipaa.html')

def iso_27701(request):
    return render(request, 'website/iso_27701.html')

def gdpr(request):
    return render(request, 'website/gdpr.html')

def soc2(request):
    return render(request, 'website/soc2.html')

def dpdp(request):
    return render(request, 'website/dpdp.html')

def iso_27017(request):
    return render(request, 'website/iso_27017.html')

def iso_27018(request):
    return render(request, 'website/iso_27018.html')

def it_general_control_audit(request):
    return render(request, 'website/it_general_control_audit.html')

def third_party_vendor_audit(request):
    return render(request, 'website/third_party_vendor_audit.html')

# Cybersecurity Operations subsections
def network_architecture_review(request):
    return render(request, 'website/network_architecture_review.html')

def brand_exploitation(request):
    return render(request, 'website/brand_exploitation.html')

# Training & Awareness subsections
def phishing_simulation(request):
    return render(request, 'website/phishing_simulation.html')

def employee_awareness_training(request):
    return render(request, 'website/employee_awareness_training.html')

# Additional Cyber Defense subsection views
def api_security_assessment(request):
    return render(request, 'website/api_security_assessment.html')

def wireless_device_security(request):
    return render(request, 'website/wireless_device_security.html')

def cloud_security_testing(request):
    return render(request, 'website/cloud_security_testing.html')

def source_code_review(request):
    return render(request, 'website/source_code_review.html')

def ot_iot_security(request):
    return render(request, 'website/ot_iot_security.html')

# Additional Governance, Risk & Compliance subsection views
def iso_27701(request):
    return render(request, 'website/iso_27701.html')

def gdpr(request):
    return render(request, 'website/gdpr.html')

def soc2(request):
    return render(request, 'website/soc2.html')

def dpdp(request):
    return render(request, 'website/dpdp.html')

def iso_27017(request):
    return render(request, 'website/iso_27017.html')

def iso_27018(request):
    return render(request, 'website/iso_27018.html')

def it_general_control_audit(request):
    return render(request, 'website/it_general_control_audit.html')

def third_party_vendor_audit(request):
    return render(request, 'website/third_party_vendor_audit.html')

# Additional Cybersecurity Operations subsection view
def brand_exploitation(request):
    return render(request, 'website/brand_exploitation.html')

def policygenerator(request):
    return render(request, 'website/policygenerator.html')


def export_pdf(request):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    
    # Create the PDF object, using the buffer as its "file"
    p = canvas.Canvas(buffer)
    
    # Draw things on the PDF
    p.drawString(100, 800, "Asset Inventory Report")
    y = 750
    # Add headers
    p.drawString(100, y, "Asset Name")
    p.drawString(250, y, "Description")
    p.drawString(400, y, "Status")
    y -= 20
    
    # Add sample data (replace with your actual data)
    sample_data = [
        ["AMZN-EC2-Linux-App", "Server that is installed in project", "Running"],
        # Add more rows as needed
    ]
    
    for row in sample_data:
        p.drawString(100, y, row[0])
        p.drawString(250, y, row[1])
        p.drawString(400, y, row[2])
        y -= 20
    
    # Close the PDF object cleanly
    p.showPage()
    p.save()
    
    # Get the value of the BytesIO buffer and return it
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="asset_inventory.pdf"'
    response.write(pdf)
    return response

def export_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="asset_inventory.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Asset Name', 'Description', 'Status'])
    
    # Add sample data (replace with your actual data)
    sample_data = [
        ['AMZN-EC2-Linux-App', 'Server that is installed in project', 'Running'],
        # Add more rows as needed
    ]
    
    for row in sample_data:
        writer.writerow(row)
    
    return response