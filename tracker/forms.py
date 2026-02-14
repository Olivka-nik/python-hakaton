"""Forms for authentication and CRUD operations."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Task


class SignUpForm(UserCreationForm):
    """Registration form with required email."""

    email = forms.EmailField(required=True)

    class Meta:
        """Metadata for signup form."""

        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit: bool = True) -> User:
        """Persist new user with email field."""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating user profile data."""

    class Meta:
        """Metadata for user update form."""

        model = User
        fields = ("username", "email")


class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks."""

    class Meta:
        """Metadata for task form."""

        model = Task
        fields = ("title", "description", "priority", "due_date", "status")
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }
