from django import forms
from .models import ContactSubmission
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'company', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-dark border border-gray-700 rounded-lg focus:ring-2 focus:ring-secondary focus:border-secondary text-white',
                'placeholder': 'John Doe'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'bg-dark border border-gray-700 rounded-lg focus:ring-2 focus:ring-secondary focus:border-secondary text-white',
                'placeholder': 'you@example.com'
            }),
            'company': forms.TextInput(attrs={
                'class': 'bg-dark border border-gray-700 rounded-lg focus:ring-2 focus:ring-secondary focus:border-secondary text-white',
                'placeholder': 'Your Company'
            }),
            'message': forms.Textarea(attrs={
                'class': 'bg-dark border border-gray-700 rounded-lg focus:ring-2 focus:ring-secondary focus:border-secondary text-white',
                'placeholder': 'Tell us how we can help...',
                'rows': 4
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Message', 
                                      css_class='w-full bg-secondary hover:bg-[#6e3691] text-white font-medium py-3 px-4 rounded-lg transition-colors'))
        self.helper.layout = Layout(
            Field('name', css_class='mb-3'),
            Field('email', css_class='mb-3'),
            Field('company', css_class='mb-3'),
            Field('message', css_class='mb-3'),
        )