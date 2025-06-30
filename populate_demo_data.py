import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poland_study_agency.settings')
django.setup()

from django.contrib.auth.models import User
from profiles.models import Profile, Milestone, ProfileMilestone

from django.utils import timezone

# Clean up old data
User.objects.filter(username__startswith='client').delete()
Milestone.objects.all().delete()

# Create milestones from the checklist
checklist_items = [
    ("Passport", "Must be valid at least 90 days after visa expiration, not older than 10 years, with at least two blank pages."),
    ("Visa Application Form & Photo", "Fully completed and signed application form with a recent 35x45mm color photo on a white background."),
    ("Applicant's Covering Letter", "A letter mentioning the purpose and duration of travel, and a list of attached documents."),
    ("Work Permit", "Original and a copy of the valid work permit."),
    ("Proof of Company Registration", "Document proving the registration of the employing company in Poland."),
    ("Employment Letter", "Original letter from the employer in Poland detailing position, salary, duration, and other conditions like accommodation."),
    ("Flight Itinerary", "Reservation only, not a purchased ticket."),
    ("Travel Medical Insurance", "Minimum coverage of 30,000 EUR, valid in the Schengen area for the entire duration of the stay."),
    ("Proof of Accommodation", "Document confirming accommodation in Poland for the intended period of stay."),
    ("Proof of Financial Solvency", "Personal bank statements from the last 3 months."),
    ("Residence Proof", "An official document proving legal stay in the current jurisdiction."),
    ("Passport Data Pages Copy", "One copy of the applicant's passport data pages (first and last) and any previous Schengen/Polish visas."),
    ("Professional/Educational Certificates (Supporting)", "Legalized/attested copies and originals."),
    ("Work Experience Certificate (Supporting)", "Copies and originals."),
    ("Police Clearance Certificate (Supporting)", "Required document to prove no criminal record."),
    ("Curriculum Vitae (CV) (Supporting)", "The applicant's CV."),
]

milestones = [Milestone.objects.create(name=name, description=desc) for name, desc in checklist_items]

# Create users
for i in range(1, 4):
    username = f'client{i}'
    password = 'password'
    user = User.objects.create_user(username=username, password=password, is_staff=True, last_login=timezone.now())
    profile = Profile.objects.create(user=user)


    # Assign milestones to profiles
    for milestone in milestones:
        ProfileMilestone.objects.create(profile=profile, milestone=milestone)

