from django.db import models
from django.contrib.auth.models import User


class Pet(models.Model):
    TYPES = [('Dog', 'Dog'), ('Cat', 'Cat'), ('Bird', 'Bird'), ('Rabbit', 'Rabbit'), ('Other', 'Other')]
    GENDERS = [('Male', 'Male'), ('Female', 'Female')]
    STATUS = [('Available', 'Available'), ('Adopted', 'Adopted')]

    name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=20, choices=TYPES)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(help_text="Age in years")
    gender = models.CharField(max_length=10, choices=GENDERS)
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_available(self):
        return self.status == 'Available'


class AdoptionRequest(models.Model):
    STATUS = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    phone = models.CharField(max_length=20)
    address = models.TextField()
    reason = models.TextField()
    previous_pet_experience = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'pet'],
                condition=models.Q(status='Pending'),
                name='unique_pending_request_per_user_pet',
            )
        ]

    def __str__(self):
        return f"{self.user} -> {self.pet} ({self.status})"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'pet'], name='unique_favorite_per_user_pet')
        ]

    def __str__(self):
        return f"{self.user} ♥ {self.pet}"
