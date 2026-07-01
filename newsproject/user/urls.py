"""URL patterns for the user app."""

from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/<int:user_id>/", views.ProfileView.as_view(), name="profile"),
    path("dashboard/<int:user_id>/", views.DashboardView.as_view(), name="dashboard"),
    # Merged settings + password + delete into one SettingsView (GET/POST split).
    path("settings/<int:user_id>/", views.SettingsView.as_view(), name="settings"),
    path("settings/<int:user_id>/password/", views.ChangePasswordView.as_view(), name="change_password"),
    path("settings/<int:user_id>/delete/", views.DeleteAccountView.as_view(), name="delete_account"),
]
