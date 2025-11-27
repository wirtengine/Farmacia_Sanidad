from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Define los roles correctos
    ROLES = [
        ('administrador', 'Administrador'),
        ('doctor', 'Doctor'),
        ('doctora', 'Doctora'),
        ('vendedor', 'Vendedor'),
        ('vendedora', 'Vendedora'),
    ]

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='vendedor'  # Puedes cambiar el valor por defecto si quieres
    )

    class Meta:
        app_label = 'usuarios'