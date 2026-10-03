from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from pets.models import AdoptionRequest, Pet
from pets.services import approve_adoption_request, create_adoption_request


class AdoptionBusinessLogicTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="rahim", password="testpass123")
        self.other_user = get_user_model().objects.create_user(username="karim", password="testpass123")
        self.pet = Pet.objects.create(
            name="Max",
            animal_type=Pet.AnimalType.DOG,
            breed="Golden Retriever",
            age=2,
            gender=Pet.Gender.MALE,
            location="Dhaka",
            description="Friendly dog",
        )

    def request_data(self):
        return {
            "address": "Dhaka",
            "phone": "+8801700000000",
            "reason": "I can provide a loving home.",
            "previous_pet_experience": True,
            "message": "Please consider my application.",
        }

    def test_only_available_pet_can_be_adopted(self):
        self.pet.status = Pet.Status.ADOPTED
        self.pet.save(update_fields=["status"])
        with self.assertRaises(ValidationError):
            create_adoption_request(user=self.user, pet=self.pet, **self.request_data())

    def test_user_cannot_create_two_pending_requests_for_same_pet(self):
        create_adoption_request(user=self.user, pet=self.pet, **self.request_data())
        with self.assertRaises(ValidationError):
            create_adoption_request(user=self.user, pet=self.pet, **self.request_data())

    def test_approval_adopts_pet_and_rejects_other_pending_requests(self):
        first = create_adoption_request(user=self.user, pet=self.pet, **self.request_data())
        second = create_adoption_request(user=self.other_user, pet=self.pet, **self.request_data())

        approve_adoption_request(first)
        first.refresh_from_db()
        second.refresh_from_db()
        self.pet.refresh_from_db()

        self.assertEqual(first.status, AdoptionRequest.Status.APPROVED)
        self.assertEqual(second.status, AdoptionRequest.Status.REJECTED)
        self.assertEqual(self.pet.status, Pet.Status.ADOPTED)
