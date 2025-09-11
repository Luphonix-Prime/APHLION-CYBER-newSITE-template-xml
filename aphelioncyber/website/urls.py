from django.urls import path
from . import views

# Add this import at the top
from django.contrib.auth.views import LoginView

# Update the urlpatterns list
urlpatterns = [
    path('', views.home, name='home'),
    path('platform/', views.platform, name='platform'),
    path('managed-security/', views.managed_security, name='managed_security'),
    path('cyber-defense/', views.cyber_defense, name='cyber_defense'),
    path('cybersecurity-operations/', views.cybersecurity_operations, name='cybersecurity_operations'),
    path('training-awareness/', views.training_awareness, name='training_awareness'),
    path('pricing/', views.pricing, name='pricing'),
    path('resources/', views.resources, name='resources'),
    path('company/', views.company, name='company'),
    # Update the login path to include 'accounts' prefix
    path('accounts/login/', LoginView.as_view(template_name='website/login.html'), name='login'),
    path('contact/', views.contact, name='contact'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('signup/', views.signup, name='signup'),  # Add this line
    path('security/', views.security, name='security'),
    path('compliance/', views.compliance, name='compliance'),
    path('addons/', views.addons, name='addons'),
    
    path('policy-generator/', views.policygenerator, name='policygenerator'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
    path('export-excel/', views.export_excel, name='export_excel'),
    
    # Managed Security Services subsections
    path('incident-response/', views.incident_response, name='incident_response'),
    path('deep-web-monitoring/', views.deep_web_monitoring, name='deep_web_monitoring'),
    path('security-operations-center/', views.security_operations_center, name='security_operations_center'),
    path('identity-access-management/', views.identity_access_management, name='identity_access_management'),
    path('third-party-risk-management/', views.third_party_risk_management, name='third_party_risk_management'),
    
    # Cyber Defense subsections
    path('vapt/', views.vapt, name='vapt'),
    path('website-application-security/', views.website_application_security, name='website_application_security'),
    path('mobile-application-security/', views.mobile_application_security, name='mobile_application_security'),
    path('api-security-assessment/', views.api_security_assessment, name='api_security_assessment'),
    path('wireless-device-security/', views.wireless_device_security, name='wireless_device_security'),
    path('cloud-security-testing/', views.cloud_security_testing, name='cloud_security_testing'),
    path('source-code-review/', views.source_code_review, name='source_code_review'),
    path('ot-iot-security/', views.ot_iot_security, name='ot_iot_security'),
    
    # Governance, Risk & Compliance subsections
    path('iso-27001/', views.iso_27001, name='iso_27001'),
    path('hipaa/', views.hipaa, name='hipaa'),
    path('iso-27701/', views.iso_27701, name='iso_27701'),
    path('gdpr/', views.gdpr, name='gdpr'),
    path('soc2/', views.soc2, name='soc2'),
    path('dpdp/', views.dpdp, name='dpdp'),
    path('iso-27017/', views.iso_27017, name='iso_27017'),
    path('iso-27018/', views.iso_27018, name='iso_27018'),
    path('it-general-control-audit/', views.it_general_control_audit, name='it_general_control_audit'),
    path('third-party-vendor-audit/', views.third_party_vendor_audit, name='third_party_vendor_audit'),
    
    # Cybersecurity Operations subsections
    path('network-architecture-review/', views.network_architecture_review, name='network_architecture_review'),
    path('brand-exploitation/', views.brand_exploitation, name='brand_exploitation'),
    
    # Training & Awareness subsections
    path('phishing-simulation/', views.phishing_simulation, name='phishing_simulation'),
    path('employee-awareness-training/', views.employee_awareness_training, name='employee_awareness_training'),
]