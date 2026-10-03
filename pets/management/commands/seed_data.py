from django.core.management.base import BaseCommand

from pets.models import Pet


SAMPLE_PETS = [
    {
        "name": "Max",
        "animal_type": Pet.AnimalType.DOG,
        "breed": "Golden Retriever",
        "age": 2,
        "gender": Pet.Gender.MALE,
        "location": "Dhaka",
        "description": "Max is friendly, playful, and loves spending time with people.",
    },
    {
        "name": "Luna",
        "animal_type": Pet.AnimalType.CAT,
        "breed": "Domestic Shorthair",
        "age": 1,
        "gender": Pet.Gender.FEMALE,
        "location": "Narayanganj",
        "description": "Luna is calm, affectionate, and enjoys a quiet home.",
    },
    {
        "name": "Coco",
        "animal_type": Pet.AnimalType.BIRD,
        "breed": "Budgerigar",
        "age": 1,
        "gender": Pet.Gender.MALE,
        "location": "Chattogram",
        "description": "Coco is energetic and social with a curious personality.",
    },
    {
        "name": "Milo",
        "animal_type": Pet.AnimalType.RABBIT,
        "breed": "Mini Lop",
        "age": 3,
        "gender": Pet.Gender.MALE,
        "location": "Gazipur",
        "description": "Milo is gentle and would do well with a caring family.",
    },
    {
        "name": "Bella",
        "animal_type": Pet.AnimalType.DOG,
        "breed": "Labrador Mix",
        "age": 4,
        "gender": Pet.Gender.FEMALE,
        "location": "Dhaka",
        "description": "Bella is loyal, friendly, and enjoys walks and play.",
    },
    {
        "name": "Simba",
        "animal_type": Pet.AnimalType.CAT,
        "breed": "Tabby",
        "age": 2,
        "gender": Pet.Gender.MALE,
        "location": "Sylhet",
        "description": "Simba is playful and curious and enjoys interactive toys.",
    },
]


class Command(BaseCommand):
    help = "Create sample pets for development/demo purposes."

    def handle(self, *args, **options):
        created = 0
        for item in SAMPLE_PETS:
            _, was_created = Pet.objects.get_or_create(name=item["name"], defaults=item)
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created} sample pets."))
