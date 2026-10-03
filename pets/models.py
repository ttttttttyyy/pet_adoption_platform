from django.conf import settings
from django.db import models
from django.db.models import Q


class Pet(models.Model):
    class AnimalType(models.TextChoices):
        DOG = "dog", "Dog"
        CAT = "cat", "Cat"
        BIRD = "bird", "Bird"
        RABBIT = "rabbit", "Rabbit"
        OTHER = "other", "Other"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        ADOPTED = "adopted", "Adopted"

    name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=20, choices=AnimalType.choices)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(help_text="Age in years")
    gender = models.CharField(max_length=10, choices=Gender.choices)
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="pets/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["animal_type", "status"], name="pets_pet_animal_status_idx"),
            models.Index(fields=["gender", "location"], name="pets_pet_gender_location_idx"),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_animal_type_display()})"


class AdoptionRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="adoption_requests")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="adoption_requests")
    address = models.TextField()
    phone = models.CharField(max_length=30)
    reason = models.TextField()
    previous_pet_experience = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "pet"],
                condition=Q(status="pending"),
                name="uniq_pending_adoption_per_user_pet",
            )
        ]
        indexes = [
            models.Index(fields=["user", "status"], name="pets_adoption_user_status_idx"),
            models.Index(fields=["pet", "status"], name="pets_adoption_pet_status_idx"),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.pet.name} ({self.get_status_display()})"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "pet"], name="uniq_favorite_user_pet")
        ]

    def __str__(self):
        return f"{self.user.username} ♥ {self.pet.name}"
