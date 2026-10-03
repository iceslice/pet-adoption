from django.contrib import admin, messages
from .models import Pet, AdoptionRequest, Favorite


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type', 'breed', 'gender', 'location', 'status')
    list_filter = ('animal_type', 'gender', 'status')
    search_fields = ('name', 'breed', 'location')
    list_editable = ('status',)


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'created_at', 'phone', 'reason', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'pet__name', 'phone')
    actions = ['approve', 'reject']

    def save_model(self, request, obj, form, change):
        """Rule 3 when status is changed through the edit form."""
        super().save_model(request, obj, form, change)
        if obj.status == 'Approved' and obj.pet.status != 'Adopted':
            obj.pet.status = 'Adopted'
            obj.pet.save()

    @admin.action(description="Approve selected requests")
    def approve(self, request, queryset):
        for req in queryset.filter(status='Pending'):
            if req.pet.status == 'Adopted':
                self.message_user(request, f"{req.pet} is already adopted.", messages.WARNING)
                continue
            req.status = 'Approved'
            req.save()
            req.pet.status = 'Adopted'
            req.pet.save()

    @admin.action(description="Reject selected requests")
    def reject(self, request, queryset):
        queryset.filter(status='Pending').update(status='Rejected')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'created_at')
    search_fields = ('user__username', 'pet__name')
