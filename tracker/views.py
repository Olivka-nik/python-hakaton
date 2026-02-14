"""Views (controller layer) for task tracker."""

from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import SignUpForm, TaskForm, UserUpdateForm
from .models import Task


class HomeView(TemplateView):
    """Show registered users and their tasks on main page."""

    template_name = "home.html"

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Build context with users and prefetched tasks."""
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.prefetch_related("tasks").all()
        return context


class SignUpView(CreateView):
    """Register new user accounts."""

    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class TaskQuerysetMixin(LoginRequiredMixin):
    """Restrict task access for non-admin users."""

    def get_queryset(self):  # type: ignore[override]
        """Return tasks visible for current user."""
        queryset = Task.objects.select_related("owner")
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(owner=self.request.user)


class TaskListView(TaskQuerysetMixin, ListView):
    """Display tasks for current user or all tasks for admin."""

    model = Task
    template_name = "tracker/task_list.html"
    context_object_name = "tasks"


class TaskCreateView(LoginRequiredMixin, CreateView):
    """Create new task for current user."""

    model = Task
    form_class = TaskForm
    template_name = "tracker/task_form.html"
    success_url = reverse_lazy("task-list")

    def form_valid(self, form: TaskForm) -> HttpResponse:
        """Attach current user as task owner before save."""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(TaskQuerysetMixin, UpdateView):
    """Edit existing task."""

    model = Task
    form_class = TaskForm
    template_name = "tracker/task_form.html"
    success_url = reverse_lazy("task-list")


class TaskDeleteView(TaskQuerysetMixin, DeleteView):
    """Delete existing task."""

    model = Task
    template_name = "tracker/task_confirm_delete.html"
    success_url = reverse_lazy("task-list")


class TaskCompleteView(LoginRequiredMixin, View):
    """Mark task as completed."""

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Switch task status to done if user has access."""
        queryset = Task.objects.all()
        if not request.user.is_superuser:
            queryset = queryset.filter(owner=request.user)

        task = get_object_or_404(queryset, pk=pk)
        task.status = Task.STATUS_DONE
        task.save(update_fields=["status", "updated_at"])
        return redirect("task-list")


class UserListView(LoginRequiredMixin, ListView):
    """Display all users for authenticated users."""

    model = User
    template_name = "tracker/user_list.html"
    context_object_name = "users"
    queryset = User.objects.all()


class UserDetailView(LoginRequiredMixin, DetailView):
    """Display user profile and tasks."""

    model = User
    template_name = "tracker/user_detail.html"
    context_object_name = "profile_user"

    def dispatch(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
        """Allow only self profile or admin profile access."""
        target_id = int(kwargs["pk"])
        if request.user.is_superuser or request.user.id == target_id:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("Недостаточно прав")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Update user profile."""

    model = User
    form_class = UserUpdateForm
    template_name = "tracker/user_form.html"

    def dispatch(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
        """Allow editing only self profile or any profile for admin."""
        target_id = int(kwargs["pk"])
        if request.user.is_superuser or request.user.id == target_id:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("Недостаточно прав")

    def get_success_url(self) -> str:
        """Redirect to corresponding profile detail page."""
        return str(reverse_lazy("user-detail", kwargs={"pk": self.object.pk}))


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """Delete user profile."""

    model = User
    template_name = "tracker/user_confirm_delete.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
        """Allow deleting only self profile or any profile for admin."""
        target_id = int(kwargs["pk"])
        if request.user.is_superuser or request.user.id == target_id:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("Недостаточно прав")
