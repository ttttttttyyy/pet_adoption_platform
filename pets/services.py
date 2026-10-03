from django.core.exceptions import ValidationError
from django.db import transaction

from .models import AdoptionRequest, Pet


ACTIVE_REQUEST_STATUSES = {AdoptionRequest.Status.PENDING}


def create_adoption_request(*, user, pet, **data):
    """Create an adoption request while enforcing the assignment's business rules."""
    with transaction.atomic():
        locked_pet = Pet.objects.select_for_update().get(pk=pet.pk)

        if locked_pet.status != Pet.Status.AVAILABLE:
            raise ValidationError("This pet has already been adopted and is not accepting applications.")

        if AdoptionRequest.objects.filter(
            user=user,
            pet=locked_pet,
            status=AdoptionRequest.Status.PENDING,
        ).exists():
            raise ValidationError("You already have a pending application for this pet.")

        return AdoptionRequest.objects.create(user=user, pet=locked_pet, **data)


def approve_adoption_request(request):
    """Approve one request atomically and close other pending requests for the same pet."""
    with transaction.atomic():
        locked_request = (
            AdoptionRequest.objects.select_for_update()
            .select_related("pet")
            .get(pk=request.pk)
        )
        locked_pet = Pet.objects.select_for_update().get(pk=locked_request.pet_id)

        if locked_request.status == AdoptionRequest.Status.APPROVED:
            return locked_request

        if locked_pet.status != Pet.Status.AVAILABLE:
            raise ValidationError("The pet is no longer available for adoption.")

        locked_request.status = AdoptionRequest.Status.APPROVED
        locked_request.save(update_fields=["status"])

        locked_pet.status = Pet.Status.ADOPTED
        locked_pet.save(update_fields=["status"])

        AdoptionRequest.objects.filter(
            pet=locked_pet,
            status=AdoptionRequest.Status.PENDING,
        ).exclude(pk=locked_request.pk).update(status=AdoptionRequest.Status.REJECTED)

        return locked_request
