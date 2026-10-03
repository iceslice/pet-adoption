from django.core.exceptions import ValidationError


def validate_new_request(user, pet):
    """Rules 1 and 2. Shared by the website views and the API."""
    from .models import AdoptionRequest
    if pet.status != 'Available':
        raise ValidationError("This pet has already been adopted.")
    if AdoptionRequest.objects.filter(user=user, pet=pet, status='Pending').exists():
        raise ValidationError("You already have a pending request for this pet.")
