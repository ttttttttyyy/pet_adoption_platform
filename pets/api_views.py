from django.db.models import Q
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import AdoptionRequest, Favorite, Pet
from .permissions import IsAdminOrReadOnly
from .serializers import AdoptionRequestSerializer, FavoriteSerializer, PetSerializer


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "breed", "description", "location"]
    ordering_fields = ["created_at", "name", "age"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        for field in ["animal_type", "breed", "gender", "location", "status"]:
            value = params.get(field)
            if value:
                lookup = f"{field}__iexact" if field != "breed" else "breed__icontains"
                queryset = queryset.filter(**{lookup: value})
        return queryset


class AdoptionRequestViewSet(viewsets.ModelViewSet):
    serializer_class = AdoptionRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = AdoptionRequest.objects.select_related("user", "pet")

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Favorite.objects.select_related("pet")

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pet = serializer.validated_data["pet"]
        favorite, created = Favorite.objects.get_or_create(user=request.user, pet=pet)
        data = self.get_serializer(favorite).data
        return Response(data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
