from django.contrib import admin
from .models import Medicamento, Proveedor

# Registro de Medicamentos
admin.site.register(Medicamento)

# Registro de Proveedores con configuración personalizada
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre_contacto', 'ruc', 'telefono', 'estado')
