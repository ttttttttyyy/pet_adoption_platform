from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import AdoptionRequest, Favorite, Pet
from .services import create_adoption_request


class PetSerializer(serializers.ModelSerializer):
    animal_type_display = serializers.CharField(source="get_animal_type_display", read_only=True)
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            "id", "name", "animal_type", "animal_type_display", "breed", "age", "gender",
            "gender_display", "location", "description", "image", "image_url", "status",
            "status_display", "created_at",
        ]
        read_only_fields = ["created_at", "image_url"]

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url


class AdoptionRequestSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source="pet.name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = AdoptionRequest
        fields = [
            "id", "user", "username", "pet", "pet_name", "address", "phone", "reason",
            "previous_pet_experience", "message", "status", "status_display", "created_at",
        ]
        read_only_fields = ["id", "user", "username", "status", "status_display", "created_at", "pet_name"]

    def create(self, validated_data):
        try:
            return create_adoption_request(
                user=self.context["request"].user,
                pet=validated_data.pop("pet"),
                **validated_data,
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message)

    def validate_pet(self, value):
        if value.status != Pet.Status.AVAILABLE:
            raise serializers.ValidationError("Only available pets can be adopted.")
        return value


class FavoriteSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source="pet.name", read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "pet", "pet_name", "created_at"]
        read_only_fields = ["id", "created_at", "pet_name"]
