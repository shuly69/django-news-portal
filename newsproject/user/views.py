"""
User-related views: registration, login, logout, profile, dashboard,
settings, password change, account deletion.

Security notes:
- LoginRequiredMixin is used on all views that touch user-private data.
- UserPassesTestMixin ensures a user can only edit/delete their OWN account
  (prevents horizontal privilege escalation via /user/settings/2/ etc.).
- Password change re-authenticates the session via update_session_auth_hash
  so the user is not logged out after changing their password.
"""

from __future__ import annotations

from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    update_session_auth_hash,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import CustomUserAutorizationForm, CustomUserCreationForm, UserSettingsForm
from .models import CustomUser
from articles.models import Article


class RegisterView(View):
    """
    Handles new user registration.
    Redirects to login on success instead of auto-logging in –
    this keeps the auth flow explicit and easy to extend (e.g. email verification).
    """

    template_name = "users/register.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name, {"form": CustomUserCreationForm(), "breadcrumb": "Register"})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
        return render(request, self.template_name, {"form": form, "breadcrumb": "Register"})


class LoginView(View):
    """
    Authenticates users via email + password.
    'Remember me' checkbox controls session lifetime:
      - Unchecked: session ends when browser closes.
      - Checked:   session lasts 14 days.
    """

    template_name = "users/login.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        # Redirect already authenticated users away from the login page.
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, self.template_name, {"form": CustomUserAutorizationForm(), "breadcrumb": "Login"})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CustomUserAutorizationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Persistent login only when the user explicitly opts in.
            session_duration = 1_209_600 if form.cleaned_data.get("remember_me") else 0
            request.session.set_expiry(session_duration)

            return redirect("home")
        return render(request, self.template_name, {"form": form, "breadcrumb": "Login"})


class LogoutView(View):
    """POST-only logout to prevent CSRF-based forced logouts via GET links."""

    def post(self, request: HttpRequest) -> HttpResponse:
        auth_logout(request)
        return redirect("home")

    # Graceful fallback for GET requests (e.g. direct URL visit).
    def get(self, request: HttpRequest) -> HttpResponse:
        auth_logout(request)
        return redirect("home")


class ProfileView(LoginRequiredMixin, View):
    """Public-ish profile page for a given user."""

    template_name = "users/profile.html"

    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        profile_user = get_object_or_404(CustomUser, id=user_id)
        return render(
            request,
            self.template_name,
            {"profile_user": profile_user, "breadcrumb": "Profile"},
        )


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Author dashboard showing all articles belonging to the user.
    UserPassesTestMixin prevents user A from viewing user B's dashboard.
    """

    template_name = "users/dashboard.html"

    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs["user_id"] or self.request.user.is_staff

    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        user = get_object_or_404(CustomUser, id=user_id)
        # prefetch_related pulls all articles in one extra query instead of N.
        articles = Article.objects.filter(author=user).select_related("category").order_by("-published_date")
        return render(
            request,
            self.template_name,
            {"user": user, "articles": articles, "breadcrumb": "Dashboard"},
        )


class SettingsView(LoginRequiredMixin, UserPassesTestMixin, View):
    """User settings page (GET shows form, POST saves changes)."""

    template_name = "users/settings.html"

    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs["user_id"] or self.request.user.is_staff

    def _get_user(self, user_id: int) -> CustomUser:
        return get_object_or_404(CustomUser, id=user_id)

    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        user = self._get_user(user_id)
        return render(
            request,
            self.template_name,
            {"form": UserSettingsForm(instance=user), "user": user, "breadcrumb": "Settings"},
        )

    def post(self, request: HttpRequest, user_id: int) -> HttpResponse:
        user = self._get_user(user_id)
        form = UserSettingsForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated.")
            return redirect("dashboard", user_id=user_id)
        return render(
            request,
            self.template_name,
            {"form": form, "user": user, "breadcrumb": "Settings"},
        )


class ChangePasswordView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Password change flow.
    update_session_auth_hash keeps the user logged in after a successful
    password change (Django would otherwise invalidate the session).
    """

    template_name = "users/settings.html"

    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs["user_id"] or self.request.user.is_staff

    def post(self, request: HttpRequest, user_id: int) -> HttpResponse:
        user = get_object_or_404(CustomUser, id=user_id)
        current_password = request.POST.get("current_password", "")
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        elif len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
        else:
            user.set_password(new_password)
            user.save()
            # Keeps the current session valid after password change.
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect("dashboard", user_id=user_id)

        return redirect("settings", user_id=user_id)


class DeleteAccountView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Permanently deletes a user account and all related content.
    Requires the user to be logged in as the account owner.
    """

    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs["user_id"] or self.request.user.is_staff

    def post(self, request: HttpRequest, user_id: int) -> HttpResponse:
        user = get_object_or_404(CustomUser, id=user_id)
        auth_logout(request)
        user.delete()
        messages.info(request, "Your account has been deleted.")
        return redirect("home")

    # Prevent accidental deletion via GET.
    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        return redirect("settings", user_id=user_id)
