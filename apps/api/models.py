from django.db import models
from authentication.models import User


# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'

    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)   # when it is set, it freeze the entire column
    updated_at = models.DateTimeField(auto_now=True)       # everytime update a particular row


    def __str__(self):
        return self.title


class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='notes', on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    solution = models.TextField()
    reference = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title




