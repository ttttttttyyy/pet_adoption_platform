from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.db.models import Q


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Pet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("animal_type", models.CharField(choices=[("dog", "Dog"), ("cat", "Cat"), ("bird", "Bird"), ("rabbit", "Rabbit"), ("other", "Other")], max_length=20)),
                ("breed", models.CharField(blank=True, max_length=100)),
                ("age", models.PositiveIntegerField(help_text="Age in years")),
                ("gender", models.CharField(choices=[("male", "Male"), ("female", "Female")], max_length=10)),
                ("location", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("image", models.ImageField(blank=True, null=True, upload_to="pets/")),
                ("status", models.CharField(choices=[("available", "Available"), ("adopted", "Adopted")], default="available", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="AdoptionRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("address", models.TextField()),
                ("phone", models.CharField(max_length=30)),
                ("reason", models.TextField()),
                ("previous_pet_experience", models.BooleanField(default=False)),
                ("message", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("pet", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="adoption_requests", to="pets.pet")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="adoption_requests", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("pet", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to="pets.pet")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="pet",
            index=models.Index(fields=["animal_type", "status"], name="pets_pet_animal_status_idx"),
        ),
        migrations.AddIndex(
            model_name="pet",
            index=models.Index(fields=["gender", "location"], name="pets_pet_gender_location_idx"),
        ),
        migrations.AddIndex(
            model_name="adoptionrequest",
            index=models.Index(fields=["user", "status"], name="pets_adoption_user_status_idx"),
        ),
        migrations.AddIndex(
            model_name="adoptionrequest",
            index=models.Index(fields=["pet", "status"], name="pets_adoption_pet_status_idx"),
        ),
        migrations.AddConstraint(
            model_name="adoptionrequest",
            constraint=models.UniqueConstraint(condition=Q(status="pending"), fields=("user", "pet"), name="uniq_pending_adoption_per_user_pet"),
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(fields=("user", "pet"), name="uniq_favorite_user_pet"),
        ),
    ]
