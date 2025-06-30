#!/usr/bin/env python
import os
import django
import csv
from django.utils.text import slugify
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poland_study_agency.settings')
django.setup()

from universities.models import University, StudyProgram

# Clear existing universities and programs
University.objects.all().delete()
StudyProgram.objects.all().delete()
print("Cleared existing universities and programs.")

# Read from universities.csv and populate the database
with open('universities.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['slug'] = slugify(row['name'])
        row['english_programs'] = row['english_programs'].lower() == 'true'
        if row.get('application_deadline'):
            row['application_deadline'] = datetime.strptime(row['application_deadline'], '%Y-%m-%d').date()
        else:
            row['application_deadline'] = None  # Ensure it's null if not present
        
        # Remove empty strings for non-required fields
        for key, value in row.items():
            if value == '':
                row[key] = None
                
        University.objects.create(**row)
        print(f"Created university: {row['name']}")

# Read from programs.csv and populate the database
with open('programs.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            university = University.objects.get(name=row['university_name'])
            row['university'] = university
            row['name'] = row['program_name']
            del row['university_name']
            del row['program_name']
            
            if row.get('application_deadline'):
                row['application_deadline'] = datetime.strptime(row['application_deadline'], '%Y-%m-%d').date()
            else:
                row['application_deadline'] = None

            StudyProgram.objects.create(**row)
            print(f"Created program: {row['name']}")
        except University.DoesNotExist:
            print(f"Skipping program for non-existent university: {row['university_name']}")

print(f"University and program population complete!")

