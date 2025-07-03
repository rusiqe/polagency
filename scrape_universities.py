
import os
import django
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from django.core.files.base import ContentFile
import requests

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poland_study_agency.settings')
django.setup()

from universities.models import University

def scrape_universities():
    """
    Deletes all existing universities and scrapes new data from study.gov.pl,
    including high-quality logos, using Selenium to handle dynamic content.
    """
    print("Deleting existing university data...")
    University.objects.all().delete()
    print("Existing data deleted.")

    base_url = 'https://study.gov.pl'
    studyfinder_url = f'{base_url}/studyfinder?field_area_tid=All&field_level_tid=All&field_language_tid=18'

    # Setup selenium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(studyfinder_url)
        time.sleep(5)  # Wait for the page to load dynamically

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        university_items = soup.select('.view-study-finder .views-row')
        print(f"Found {len(university_items)} universities on the page.")

        for item in university_items:
            name_tag = item.select_one('h3.title a')
            city_tag = item.select_one('.views-field-field-city .field-content')

            if name_tag and city_tag:
                name = name_tag.get_text(strip=True)
                detail_page_url = urljoin(base_url, name_tag['href'])
                city = city_tag.get_text(strip=True)

                print(f"Processing: {name} in {city}")

                # Scrape detail page for logo
                logo_url = None
                try:
                    detail_response = requests.get(detail_page_url)
                    detail_response.raise_for_status()
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                    
                    logo_img = detail_soup.select_one('.field-name-field-logo img')
                    if not logo_img:
                         logo_img = detail_soup.select_one('.logo img')

                    if logo_img and logo_img.get('src'):
                        logo_url = urljoin(base_url, logo_img['src'])
                        print(f"Found logo URL: {logo_url}")

                except requests.RequestException as e:
                    print(f"Could not fetch detail page for {name}: {e}")

                # Create University object
                uni, created = University.objects.get_or_create(
                    name=name,
                    defaults={
                        'city': city,
                        'website': detail_page_url, 
                        'university_type': 'public'
                    }
                )

                if created:
                     print(f"Created new university: {name}")
                else:
                     print(f"University {name} already exists. Updating.")


                # Download and save logo
                if logo_url and not uni.logo:
                    try:
                        logo_response = requests.get(logo_url)
                        logo_response.raise_for_status()
                        
                        file_name = os.path.basename(urlparse(logo_url).path)
                        uni.logo.save(file_name, ContentFile(logo_response.content), save=True)
                        print(f"Successfully downloaded and saved logo for {name}")

                    except requests.RequestException as e:
                        print(f"Could not download logo for {name}: {e}")

    finally:
        driver.quit()

if __name__ == '__main__':
    scrape_universities()

