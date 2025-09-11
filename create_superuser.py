import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aphelioncyber.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import IntegrityError

def create_superuser():
    User = get_user_model()
    
    try:
        # Define superuser credentials
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'
        
        # Check if superuser already exists
        if not User.objects.filter(username=username).exists():
            # Create superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f'Superuser "{username}" created successfully!')
        else:
            print(f'Superuser "{username}" already exists.')
            
    except IntegrityError as e:
        print(f'Error creating superuser: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')

if __name__ == '__main__':
    create_superuser()