
import os
import django
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poland_study_agency.settings')
django.setup()

from universities.models import University

def scrape_university_logos():
    for university in University.objects.all():
        if university.website and not university.logo:
            try:
                response = requests.get(university.website)
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find the logo (common patterns)
                logo_img = soup.find('img', alt=lambda x: x and 'logo' in x.lower())
                if not logo_img:
                    logo_img = soup.find('a', class_=lambda x: x and 'logo' in x.lower()).find('img')

                if logo_img and logo_img.has_attr('src'):
                    logo_url = urljoin(university.website, logo_img['src'])
                    logo_response = requests.get(logo_url, stream=True)

                    if logo_response.status_code == 200:
                        # Save the logo
                        logo_filename = os.path.basename(logo_url)
                        logo_path = os.path.join('media', 'universities', 'logos', logo_filename)
                        os.makedirs(os.path.dirname(logo_path), exist_ok=True)

                        with open(logo_path, 'wb') as f:
                            for chunk in logo_response.iter_content(1024):
                                f.write(chunk)

                        university.logo.name = os.path.join('universities', 'logos', logo_filename)
                        university.save()
                        print(f'Successfully downloaded logo for {university.name}')
            except Exception as e:
                print(f'Could not fetch logo for {university.name}: {e}')

if __name__ == '__main__':
    scrape_university_logos()

