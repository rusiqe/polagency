#!/usr/bin/env python
import os
import django
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poland_study_agency.settings')
django.setup()

from universities.models import University

# Clear existing universities
University.objects.all().delete()
print("Cleared existing universities.")

universities_data = [
    # Existing Universities
    {
        "name": "Jagiellonian University", "name_polish": "Uniwersytet Jagielloński", "city": "Kraków",
        "university_type": "public", "website": "https://en.uj.edu.pl/", "english_programs": True
    },
    {
        "name": "University of Warsaw", "name_polish": "Uniwersytet Warszawski", "city": "Warsaw",
        "university_type": "public", "website": "https://en.uw.edu.pl/", "english_programs": True
    },
    {
        "name": "AGH University of Science and Technology", "name_polish": "Akademia Górniczo-Hutnicza", "city": "Kraków",
        "university_type": "public", "website": "https://www.agh.edu.pl/en/", "english_programs": True
    },
    {
        "name": "Warsaw University of Technology", "name_polish": "Politechnika Warszawska", "city": "Warsaw",
        "university_type": "public", "website": "https://www.pw.edu.pl/engpw", "english_programs": True
    },
    {
        "name": "Adam Mickiewicz University, Poznań", "name_polish": "Uniwersytet im. Adama Mickiewicza w Poznaniu", "city": "Poznań",
        "university_type": "public", "website": "https://amu.edu.pl/en", "english_programs": True
    },
    # Lublin Universities
    {
        "name": "Medical University of Lublin", "name_polish": "Uniwersytet Medyczny w Lublinie", "city": "Lublin",
        "university_type": "public", "website": "https://www.umlub.pl/en/", "english_programs": True
    },
    {
        "name": "Lublin University of Technology", "name_polish": "Politechnika Lubelska", "city": "Lublin",
        "university_type": "public", "website": "https://en.pollub.pl/", "english_programs": True
    },
    {
        "name": "Vincent Pol University in Lublin", "name_polish": "Wyższa Szkoła Społeczno-Przyrodnicza im. Wincentego Pola", "city": "Lublin",
        "university_type": "private", "website": "https://vpu.edu.pl/", "english_programs": True
    },
    {
        "name": "University of Life Sciences in Lublin", "name_polish": "Uniwersytet Przyrodniczy w Lublinie", "city": "Lublin",
        "university_type": "public", "website": "https://up.lublin.pl/en/", "english_programs": True
    },
    # Wrocław Universities
    {
        "name": "University of Wrocław", "name_polish": "Uniwersytet Wrocławski", "city": "Wrocław",
        "university_type": "public", "website": "https://international.uni.wroc.pl/", "english_programs": True
    },
    {
        "name": "Wrocław University of Science and Technology", "name_polish": "Politechnika Wrocławska", "city": "Wrocław",
        "university_type": "public", "website": "https://pwr.edu.pl/en/", "english_programs": True
    },
    {
        "name": "Wrocław Medical University", "name_polish": "Uniwersytet Medyczny im. Piastów Śląskich we Wrocławiu", "city": "Wrocław",
        "university_type": "public", "website": "https://www.umw.edu.pl/pl", "english_programs": True
    },
    {
        "name": "Wrocław University of Environmental and Life Sciences", "name_polish": "Uniwersytet Przyrodniczy we Wrocławiu", "city": "Wrocław",
        "university_type": "public", "website": "https://upwr.edu.pl/en/", "english_programs": True
    },
    {
        "name": "Wrocław University of Economics and Business", "name_polish": "Uniwersytet Ekonomiczny we Wrocławiu", "city": "Wrocław",
        "university_type": "public", "website": "https://www.ue.wroc.pl/en/", "english_programs": True
    },
    {
        "name": "University of Lower Silesia", "name_polish": "Dolnośląska Szkoła Wyższa", "city": "Wrocław",
        "university_type": "private", "website": "https://www.dsw.edu.pl/en/", "english_programs": True
    }
]

for data in universities_data:
    data['slug'] = slugify(data['name'])
    University.objects.create(**data)
    print(f"Created university: {data['name']}")

print(f"University population complete! Total: {len(universities_data)} universities.")

