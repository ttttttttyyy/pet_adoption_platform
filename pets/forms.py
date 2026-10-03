from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import AdoptionRequest, Pet


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ["address", "phone", "reason", "previous_pet_experience", "message"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3, "placeholder": "Your full address"}),
            "phone": forms.TextInput(attrs={"placeholder": "+8801XXXXXXXXX"}),
            "reason": forms.Textarea(attrs={"rows": 4, "placeholder": "Why do you want to adopt this pet?"}),
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Optional additional message"}),
        }
