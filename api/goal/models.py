from django.contrib.auth.models import User
from django.db import models

from category.models import SubCategory


class Goal(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    title = models.CharField(max_length=180, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False, blank=True)
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
