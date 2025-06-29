#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poland_study_agency.settings')
django.setup()

from universities.models import University
from django.utils.text import slugify

# Clear existing universities
University.objects.all().delete()
print("Cleared existing universities.")

universities_data = [
    {
        "name": "Jagiellonian University",
        "name_polish": "Uniwersytet Jagielloński",
        "city": "Kraków",
        "university_type": "public",
        "description": "One of the oldest and most prestigious universities in the world, founded in 1364.",
        "website": "https://en.uj.edu.pl/",
        "english_programs": True
    },
    {
        "name": "University of Warsaw",
        "name_polish": "Uniwersytet Warszawski",
        "city": "Warsaw",
        "university_type": "public",
        "description": "Poland’s largest and finest university, offering a wide range of programs and research opportunities.",
        "website": "https://en.uw.edu.pl/",
        "english_programs": True
    },
    {
        "name": "AGH University of Science and Technology",
        "name_polish": "Akademia Górniczo-Hutnicza im. Stanisława Staszica w Krakowie",
        "city": "Kraków",
        "university_type": "public",
        "description": "A leading technical university with a focus on engineering, technology, and applied sciences.",
        "website": "https://www.agh.edu.pl/en/",
        "english_programs": True
    },
    {
        "name": "Warsaw University of Technology",
        "name_polish": "Politechnika Warszawska",
        "city": "Warsaw",
        "university_type": "public",
        "description": "One of the largest and highest-ranking technological universities in Central Europe.",
        "website": "https://www.pw.edu.pl/engpw",
        "english_programs": True
    },
    {
        "name": "Adam Mickiewicz University in Poznań",
        "name_polish": "Uniwersytet im. Adama Mickiewicza w Poznaniu",
        "city": "Poznań",
        "university_type": "public",
        "description": "A major Polish university, known for its strong programs in humanities and social sciences.",
        "website": "https://amu.edu.pl/en",
        "english_programs": True
    }
]

for data in universities_data:
    data['slug'] = slugify(data['name'])
    University.objects.create(**data)
    print(f"Created university: {data['name']}")

print("University population complete!")

