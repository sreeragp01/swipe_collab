from django.conf import settings
from django.db import models


class Workspace(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_ON_HOLD = "on_hold"
    STATUS_COMPLETED = "completed"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_ON_HOLD, "On Hold"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workspaces",
    )
    match = models.ForeignKey(
        "matches.Match",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workspaces",
    )
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_workspaces",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="joined_workspaces",
        blank=True,
    )
    progress_percent = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workspaces_workspace"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.title} ({self.status})"

    def recalculate_progress(self):
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            self.progress_percent = 0
        else:
            completed = self.tasks.filter(status=Task.STATUS_COMPLETED).count()
            self.progress_percent = int((completed / total_tasks) * 100)
        self.save(update_fields=["progress_percent"])


class Task(models.Model):
    STATUS_TODO = "todo"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_IN_REVIEW = "in_review"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_TODO, "To Do"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_IN_REVIEW, "In Review"),
        (STATUS_COMPLETED, "Completed"),
    ]

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_URGENT = "urgent"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
        (PRIORITY_URGENT, "Urgent"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO)
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workspaces_task"
        ordering = ["created_at"]

    def __str__(self):
        return f"Task: {self.title} [{self.status}]"


class WorkspaceFile(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="files",
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_workspace_files",
    )
    title = models.CharField(max_length=255)
    file_url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to="workspace_files/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "workspaces_file"
        ordering = ["-created_at"]

    def __str__(self):
        return f"File: {self.title} in {self.workspace.title}"
