"""
User-related forms: registration, login, profile settings.

Key design decisions:
- CustomUserCreationForm inherits from UserCreationForm (not ModelForm) so
  Django's built-in password matching and strength validation runs automatically.
  Previously it used ModelForm which skipped password2 validation entirely.
- CustomUserAutorizationForm inherits from AuthenticationForm to reuse
  Django's secure credential checking logic.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Registration form.

    Inherits from UserCreationForm so Django automatically:
      - validates that password1 == password2
      - runs all AUTH_PASSWORD_VALIDATORS (length, common passwords, etc.)
      - calls set_password() before saving
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-input", "placeholder": "Enter your email", "id": "email"}
        ),
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-textarea", "placeholder": "Tell us about yourself", "rows": 4}
        ),
    )
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Choose a username", "id": "username"}
        ),
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "First Name", "id": "firstName"}
        ),
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Last Name", "id": "lastName"}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-input", "placeholder": "Enter your password", "id": "password"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={"class": "form-input", "placeholder": "Confirm your password", "id": "confirmPassword"}
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["username", "email", "bio", "specialization", "first_name", "last_name"]
        widgets = {
            "specialization": forms.Select(attrs={"class": "form-select", "id": "specialization"}),
        }


class CustomUserAutorizationForm(AuthenticationForm):
    """
    Login form using email as the username field.
    AuthenticationForm handles credential validation and brute-force
    protection via Django's authentication backend.
    """

    username = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-input", "placeholder": "Enter your email", "id": "email"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-input", "placeholder": "Enter your password", "id": "password"}
        ),
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"id": "rememberMe"}),
    )

    class Meta:
        model = CustomUser


class UserSettingsForm(forms.ModelForm):
    """Form for updating profile information (not password)."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-input", "placeholder": "Enter your email", "id": "email"}
        ),
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-textarea", "placeholder": "Tell us about yourself", "rows": 4}
        ),
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "First Name", "id": "firstName"}
        ),
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Last Name", "id": "lastName"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "bio", "specialization"]
        widgets = {
            "specialization": forms.Select(attrs={"class": "form-select", "id": "specialization"}),
        }
