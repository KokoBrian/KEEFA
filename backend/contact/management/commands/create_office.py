from django.core.management.base import BaseCommand
from contact.models import OfficeLocation

class Command(BaseCommand):
    help = 'Create a default office location'

    def handle(self, *args, **kwargs):
        if OfficeLocation.objects.filter(name="Main Office").exists():
            self.stdout.write(self.style.WARNING("Main Office already exists."))
            return
        
        office = OfficeLocation.objects.create(
            name="Main Office",
            address="123 Main St",
            city="Nairobi",
            county="Nairobi County",
            postal_code="00100",
            country="Kenya",
            phone="123-456-7890",
            email="mainoffice@example.com",
            fax="123-456-7891",
            latitude= -1.2921,   # Nairobi approx latitude
            longitude=36.8219,   # Nairobi approx longitude
            office_hours="Mon-Fri 9am-5pm",
            services_offered="General inquiries, donations, volunteering",
            is_main_office=True,
            is_public=True,
            order=1,
        )
        
        self.stdout.write(self.style.SUCCESS(f"Office '{office.name}' created successfully!"))
