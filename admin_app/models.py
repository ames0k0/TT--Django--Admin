from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser
    """
    phone_number = models.CharField(_("Phone number"), max_length=15, blank=True)
    address = models.TextField(_("Address"), blank=True)
    birth_date = models.DateField(_("Birth date"), null=True, blank=True)
    profile_picture = models.ImageField(_("Profile picture"), upload_to='profile_pics/', null=True, blank=True)
    is_verified = models.BooleanField(_("Verified"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['-date_joined']
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.get_full_name() or self.username

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
