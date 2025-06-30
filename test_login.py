import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poland_study_agency.settings')
django.setup()

from django.contrib.auth import authenticate

user = authenticate(username='client1', password='password')

if user is not None:
    print('Login successful for client1')
else:
    print('Login failed for client1')

