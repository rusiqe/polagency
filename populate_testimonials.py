#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poland_study_agency.settings')
django.setup()

from services.models import Testimonial

# Clear existing testimonials
Testimonial.objects.all().delete()
print("Cleared existing testimonials.")

testimonials_data = [
    {
        "name": "Amina Yusuf",
        "testimonial_text": "The milestone payment structure was a lifesaver. It made the whole process financially manageable. The team's guidance for my Nursing application was flawless, and their support during the visa stage was incredible. I couldn't have done it without them!",
        "rating": 5,
        "program": "BSc Nursing"
    },
    {
        "name": "John Omondi",
        "testimonial_text": "I was looking for a top-tier Data Science program, and this agency delivered. They found the perfect MSc program for me and handled all the application complexities. The post-arrival support, especially the TRC assistance, was beyond helpful.",
        "rating": 5,
        "program": "MSc Data Science"
    },
    {
        "name": "Sandra Williams",
        "testimonial_text": "From choosing the right Computer Science university to the final airport pickup, the process was seamless. The free consultation call for me and my parents was very reassuring. A truly professional and trustworthy agency for any aspiring student.",
        "rating": 5,
        "program": "BSc Computer Science"
    }
]

for data in testimonials_data:
    Testimonial.objects.create(**data)
    print(f"Created testimonial for {data['name']}")

print("New testimonial population complete!")

