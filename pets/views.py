from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import AdoptionForm, RegisterForm
from .models import AdoptionRequest, Favorite, Pet
from .services import validate_new_request


def _favorite_ids(request):
    if not request.user.is_authenticated:
        return set()
    return set(Favorite.objects.filter(user=request.user).values_list('pet_id', flat=True))


def home(request):
    pets = Pet.objects.filter(status='Available')[:3]
    return render(request, 'pets/home.html', {'pets': pets, 'favorite_ids': _favorite_ids(request)})


def pet_list(request):
    pets = Pet.objects.all()
    g = request.GET

    if g.get('q'):
        pets = pets.filter(name__icontains=g['q'])
    if g.get('animal_type'):
        pets = pets.filter(animal_type=g['animal_type'])
    if g.get('breed'):
        pets = pets.filter(breed__icontains=g['breed'])
    if g.get('gender'):
        pets = pets.filter(gender=g['gender'])
    if g.get('location'):
        pets = pets.filter(location__icontains=g['location'])
    if g.get('status'):
        pets = pets.filter(status=g['status'])

    page_obj = Paginator(pets, 6).get_page(g.get('page'))

    params = g.copy()
    params.pop('page', None)

    return render(request, 'pets/pet_list.html', {
        'page_obj': page_obj,
        'querystring': params.urlencode(),
        'animal_types': Pet.TYPES,
        'genders': Pet.GENDERS,
        'statuses': Pet.STATUS,
        'favorite_ids': _favorite_ids(request),
    })


def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    has_pending = (
        request.user.is_authenticated
        and AdoptionRequest.objects.filter(user=request.user, pet=pet, status='Pending').exists()
    )
    return render(request, 'pets/pet_detail.html', {
        'pet': pet,
        'has_pending': has_pending,
        'favorite_ids': _favorite_ids(request),
    })


@login_required
def apply(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    try:
        validate_new_request(request.user, pet)
    except ValidationError as e:
        messages.error(request, e.messages[0])
        return redirect('pet_detail', pk=pet.pk)

    if request.method == 'POST':
        form = AdoptionForm(request.POST)
        if form.is_valid():
            adoption = form.save(commit=False)
            adoption.user = request.user
            adoption.pet = pet
            try:
                adoption.save()
            except IntegrityError:
                messages.error(request, "You already have a pending request for this pet.")
                return redirect('pet_detail', pk=pet.pk)
            messages.success(request, f"Your application for {pet.name} was submitted.")
            return redirect('my_requests')
    else:
        form = AdoptionForm()

    return render(request, 'pets/apply.html', {'form': form, 'pet': pet})


@login_required
def my_requests(request):
    requests_qs = AdoptionRequest.objects.filter(user=request.user).select_related('pet')
    return render(request, 'pets/my_requests.html', {'adoption_requests': requests_qs})


@login_required
def profile(request):
    return render(request, 'pets/profile.html', {
        'request_count': AdoptionRequest.objects.filter(user=request.user).count(),
        'favorite_count': Favorite.objects.filter(user=request.user).count(),
    })


@login_required
@require_POST
def toggle_favorite(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, pet=pet)
    if created:
        messages.success(request, f"{pet.name} added to your favorites.")
    else:
        fav.delete()
        messages.info(request, f"{pet.name} removed from your favorites.")

    next_url = request.POST.get('next', '')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('pet_detail', pk=pet.pk)


@login_required
def favorites(request):
    pets = Pet.objects.filter(favorited_by__user=request.user).order_by('-favorited_by__created_at')
    return render(request, 'pets/favorites.html', {
        'pets': pets,
        'favorite_ids': _favorite_ids(request),
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('pet_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect('pet_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
