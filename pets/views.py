from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from .forms import AdoptionRequestForm, RegisterForm
from .models import AdoptionRequest, Favorite, Pet
from .services import create_adoption_request


def home(request):
    featured_pets = Pet.objects.filter(status=Pet.Status.AVAILABLE)[:6]
    return render(request, "pets/home.html", {"featured_pets": featured_pets})


def pet_list(request):
    pets = Pet.objects.all()
    q = request.GET.get("q", "").strip()
    animal_type = request.GET.get("animal_type", "")
    breed = request.GET.get("breed", "").strip()
    gender = request.GET.get("gender", "")
    location = request.GET.get("location", "").strip()
    status = request.GET.get("status", "")

    if q:
        pets = pets.filter(Q(name__icontains=q) | Q(breed__icontains=q) | Q(description__icontains=q) | Q(location__icontains=q))
    if animal_type:
        pets = pets.filter(animal_type=animal_type)
    if breed:
        pets = pets.filter(breed__icontains=breed)
    if gender:
        pets = pets.filter(gender=gender)
    if location:
        pets = pets.filter(location__icontains=location)
    if status:
        pets = pets.filter(status=status)

    paginator = Paginator(pets, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    query_params = request.GET.copy()
    query_params.pop("page", None)
    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(Favorite.objects.filter(user=request.user).values_list("pet_id", flat=True))

    return render(
        request,
        "pets/pet_list.html",
        {
            "page_obj": page_obj,
            "favorite_ids": favorite_ids,
            "animal_types": Pet.AnimalType.choices,
            "genders": Pet.Gender.choices,
            "statuses": Pet.Status.choices,
            "query_string": query_params.urlencode(),
        },
    )


def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(user=request.user, pet=pet).exists()
    return render(request, "pets/pet_detail.html", {"pet": pet, "is_favorite": is_favorite})


@login_required
def adoption_create(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if pet.status != Pet.Status.AVAILABLE:
        messages.error(request, "This pet is no longer available for adoption.")
        return redirect("pet-detail", pk=pet.pk)

    if AdoptionRequest.objects.filter(user=request.user, pet=pet, status=AdoptionRequest.Status.PENDING).exists():
        messages.info(request, "You already have a pending application for this pet.")
        return redirect("dashboard")

    form = AdoptionRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            create_adoption_request(user=request.user, pet=pet, **form.cleaned_data)
        except ValidationError as exc:
            messages.error(request, exc.message)
        else:
            messages.success(request, "Your adoption application has been submitted.")
            return redirect("dashboard")

    return render(request, "pets/adoption_form.html", {"form": form, "pet": pet})


@login_required
def dashboard(request):
    requests = AdoptionRequest.objects.filter(user=request.user).select_related("pet")
    stats = {
        "total": requests.count(),
        "pending": requests.filter(status=AdoptionRequest.Status.PENDING).count(),
        "approved": requests.filter(status=AdoptionRequest.Status.APPROVED).count(),
        "rejected": requests.filter(status=AdoptionRequest.Status.REJECTED).count(),
    }
    return render(request, "pets/dashboard.html", {"requests": requests, "stats": stats})


@login_required
def profile(request):
    return render(request, "pets/profile.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created successfully. Welcome!")
        return redirect("home")
    return render(request, "registration/register.html", {"form": form})


@login_required
def favorite_toggle(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method != "POST":
        return redirect("pet-detail", pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, pet=pet)
    if not created:
        favorite.delete()
        messages.info(request, f"{pet.name} removed from favorites.")
    else:
        messages.success(request, f"{pet.name} added to favorites.")
    return redirect(request.POST.get("next") or "pet-detail", pk=pk)


@login_required
def favorites(request):
    items = Pet.objects.filter(favorites__user=request.user).order_by("-favorites__created_at")
    return render(request, "pets/favorites.html", {"pets": items})
