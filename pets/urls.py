from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("pets/", views.pet_list, name="pet-list"),
    path("pets/<int:pk>/", views.pet_detail, name="pet-detail"),
    path("pets/<int:pk>/adopt/", views.adoption_create, name="adoption-create"),
    path("pets/<int:pk>/favorite/", views.favorite_toggle, name="favorite-toggle"),
    path("favorites/", views.favorites, name="favorites"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
