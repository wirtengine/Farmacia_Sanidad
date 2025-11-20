from django import forms
from django.core.exceptions import ValidationError
from .models import Medicamento, Proveedor, Empleados, Venta

# ========================
# FORMULARIOS DE PROVEEDORES
# ========================
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre_contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del contacto'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese la dirección completa'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 8888-8888'
            }),
            'fecha_registro': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'ruc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: J-123456789-0'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[(1, 'Activo'), (0, 'Inactivo')]),
            'tipo_proveedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Distribuidor, Laboratorio, etc.'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que algunos campos no sean requeridos
        self.fields['fecha_registro'].required = False
        self.fields['ruc'].required = False
        self.fields['correo'].required = False
        self.fields['tipo_proveedor'].required = False
        self.fields['direccion'].required = False
        self.fields['telefono'].required = False

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if ruc:
            # Verificar si ya existe un proveedor con el mismo RUC
            proveedores = Proveedor.objects.filter(ruc=ruc)
            if self.instance and self.instance.pk:
                # Si estamos editando, excluir el registro actual
                proveedores = proveedores.exclude(pk=self.instance.pk)
            if proveedores.exists():
                raise ValidationError('Ya existe un proveedor con este RUC.')
        return ruc

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if correo:
            # Verificar si ya existe un proveedor con el mismo correo
            proveedores = Proveedor.objects.filter(correo=correo)
            if self.instance and self.instance.pk:
                # Si estamos editando, excluir el registro actual
                proveedores = proveedores.exclude(pk=self.instance.pk)
            if proveedores.exists():
                raise ValidationError('Ya existe un proveedor con este correo electrónico.')
        return correo

# ========================
# FORMULARIOS DE MEDICAMENTOS
# ========================
class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = '__all__'
        widgets = {
            'nombre_generico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre genérico del medicamento'
            }),
            'id_factura_compra': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha_caducidad': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'contra_indicaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese las contraindicaciones'
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cada 8 horas'
            }),
            'cod_laboratorio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: LAB-123'
            }),
            'registro_sanitario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: RS-NIC-12345'
            }),
            'precauciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese las precauciones'
            }),
            'presentacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Tabletas, Jarabe, Cápsulas'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '10'
            }),
            'via_administracion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Oral, Inyectable, Tópica'
            }),
            'requiere_receta': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[(1, 'Activo'), (0, 'Inactivo')]),
            'fecha_registro': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que algunos campos no sean requeridos
        self.fields['id_factura_compra'].required = False
        self.fields['fecha_caducidad'].required = False
        self.fields['contra_indicaciones'].required = False
        self.fields['dosis'].required = False
        self.fields['cod_laboratorio'].required = False
        self.fields['registro_sanitario'].required = False
        self.fields['precauciones'].required = False
        self.fields['presentacion'].required = False
        self.fields['via_administracion'].required = False
        self.fields['fecha_registro'].required = False

    def clean_nombre_generico(self):
        nombre_generico = self.cleaned_data.get('nombre_generico')
        if nombre_generico:
            # Verificar si ya existe un medicamento con el mismo nombre (case-insensitive)
            medicamentos = Medicamento.objects.filter(nombre_generico__iexact=nombre_generico)
            if self.instance and self.instance.pk:
                # Si estamos editando, excluir el registro actual
                medicamentos = medicamentos.exclude(pk=self.instance.pk)
            if medicamentos.exists():
                raise ValidationError('Ya existe un medicamento con este nombre genérico.')
        return nombre_generico

    def clean_registro_sanitario(self):
        registro_sanitario = self.cleaned_data.get('registro_sanitario')
        if registro_sanitario:
            # Verificar si ya existe un medicamento con el mismo registro sanitario
            medicamentos = Medicamento.objects.filter(registro_sanitario=registro_sanitario)
            if self.instance and self.instance.pk:
                # Si estamos editando, excluir el registro actual
                medicamentos = medicamentos.exclude(pk=self.instance.pk)
            if medicamentos.exists():
                raise ValidationError('Ya existe un medicamento con este registro sanitario.')
        return registro_sanitario

# ========================
# FORMULARIOS DE EMPLEADOS
# ========================
class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleados
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre completo'
            }),
            'fecha_contratacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'rol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Doctor, Vendedor, Administrador'
            }),
            'funciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa las funciones del empleado'
            }),
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 001-123456-0001A'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 8888-8888'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[(1, 'Activo'), (0, 'Inactivo')]),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que algunos campos no sean requeridos
        self.fields['fecha_contratacion'].required = False
        self.fields['rol'].required = False
        self.fields['funciones'].required = False
        self.fields['cedula'].required = False
        self.fields['telefono'].required = False
        self.fields['correo'].required = False

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if cedula:
            # Verificar si ya existe un empleado con la misma cédula
            empleados = Empleados.objects.filter(cedula=cedula)
            if self.instance and self.instance.pk:
                # Si estamos editando, excluir el registro actual
                empleados = empleados.exclude(pk=self.instance.pk)
            if empleados.exists():
                raise ValidationError('Ya existe un empleado con esta cédula.')
        return cedula

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if correo:
            # Verificar si ya existe un empleado con el mismo correo
            empleados = Empleados.objects.filter(correo=correo)
            if self.instance and self.instance.pk:
                # Si estamos editando, excluir el registro actual
                empleados = empleados.exclude(pk=self.instance.pk)
            if empleados.exists():
                raise ValidationError('Ya existe un empleado con este correo electrónico.')
        return correo

# ========================
# FORMULARIOS DE VENTAS
# ========================
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'id_cliente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'id_empleado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'descuento': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'impuesto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('Pagada', 'Pagada'),
                ('Pendiente', 'Pendiente'),
                ('Anulada', 'Anulada'),
                ('En proceso', 'En proceso')
            ]),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que algunos campos no sean requeridos
        self.fields['fecha'].required = False
        self.fields['total'].required = False
        self.fields['id_cliente'].required = False
        self.fields['id_empleado'].required = False
        self.fields['descuento'].required = False
        self.fields['impuesto'].required = False