from django.db import models
from django.utils import timezone

class Author(models.Model):
    name = models.CharField(max_length=50)
    birth_date = models.DateField()
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
