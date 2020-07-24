from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # username = models.CharField(max_length=128, unique=True, default="rajeet")
    email = models.EmailField(unique=True)
    imageFile = models.FileField(upload_to='media/', null=True, blank=True, verbose_name="")
    REQUIRED_FIELDS = []


    groups = None
    user_permissions = None

# Create your models here.
class Blogging(models.Model):
    title = models.CharField(max_length=200)
    blog_details = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user

