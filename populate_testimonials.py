#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poland_study_agency.settings')
django.setup()

from services.models import Testimonial

testimonials_data = [
    {
        "name": "Adanna Okoro",
        "testimonial_text": "The team at Poland Study Agency made my dream of studying nursing in Europe a reality. Their step-by-step guidance was invaluable, especially during the visa process. I felt supported from my first inquiry until I was settled in my dorm. Highly recommended!",
        "rating": 5
    },
    {
        "name": "David Chen",
        "testimonial_text": "I was completely lost with the application process, but their consultants broke it down into manageable steps. The milestone payments made it affordable, and the team was always available to answer my questions. A truly professional and caring agency.",
        "rating": 5
    },
    {
        "name": "Chidinma Eze",
        "testimonial_text": "As a parent, I was worried about sending my daughter abroad. The free consultation call with the agent and my daughter put all my fears to rest. They were transparent about the process and costs, and their on-ground support in Poland is fantastic.",
        "rating": 5
    }
]

for data in testimonials_data:
    if not Testimonial.objects.filter(name=data["name"]).exists():
        Testimonial.objects.create(**data)
        print(f"Created testimonial for {data['name']}")
    else:
        print(f"Testimonial for {data['name']} already exists.")

print("Testimonial population complete!")

