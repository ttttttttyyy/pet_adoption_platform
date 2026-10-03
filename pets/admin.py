from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import AdoptionRequest, Favorite, Pet
from .services import approve_adoption_request


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "animal_type", "breed", "age", "gender", "location", "status", "created_at")
    list_filter = ("animal_type", "gender", "status", "location")
    search_fields = ("name", "breed", "location", "description")
    list_editable = ("status",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "pet", "created_at", "phone", "status")
    list_filter = ("status", "created_at", "pet__animal_type")
    search_fields = ("user__username", "pet__name", "phone", "reason")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("user", "pet")

    def save_model(self, request, obj, form, change):
        previous_status = None
        if change:
            previous_status = AdoptionRequest.objects.get(pk=obj.pk).status

        if obj.status == AdoptionRequest.Status.APPROVED and previous_status != AdoptionRequest.Status.APPROVED:
            try:
                super().save_model(request, obj, form, change)
                approve_adoption_request(obj)
            except ValidationError as exc:
                self.message_user(request, exc.message, level=messages.ERROR)
                raise
            return

        super().save_model(request, obj, form, change)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "pet", "created_at")
    search_fields = ("user__username", "pet__name")
    autocomplete_fields = ("user", "pet")
    readonly_fields = ("created_at",)
