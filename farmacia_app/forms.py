from django import forms
from django.core.exceptions import ValidationError
from .models import Medicamento, Proveedor, Empleados, Venta, Lote, FacturaCompra, LoteMedicamento, Cliente, DevolucionCliente, DevolucionProveedor
from datetime import date


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
            'estado': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'fecha_registro': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔹 AÑADE 'stock_minimo' A LA LISTA DE CAMPOS OPCIONALES
        opcionales = [
            'id_factura_compra',
            'fecha_caducidad',
            'contra_indicaciones',
            'dosis',
            'cod_laboratorio',
            'registro_sanitario',
            'precauciones',
            'presentacion',
            'via_administracion',
            'fecha_registro',
            'stock_minimo'  # 🔹 ESTA ES LA LÍNEA CLAVE QUE FALTA
        ]

        for campo in opcionales:
            self.fields[campo].required = False

        # Forzar los choices reales del estado
        self.fields['estado'].choices = [
            (1, "Activo"),
            (0, "Inactivo")
        ]

    def clean_stock_minimo(self):
        """Asegurar que stock_minimo tenga un valor por defecto si está vacío"""
        stock_minimo = self.cleaned_data.get('stock_minimo')
        if not stock_minimo:
            return 10  # Valor por defecto
        return stock_minimo

    def clean_registro_sanitario(self):
        registro_sanitario = self.cleaned_data.get('registro_sanitario')

        if registro_sanitario:
            medicamentos = Medicamento.objects.filter(
                registro_sanitario=registro_sanitario
            )

            # Si estamos editando, excluir el actual
            if self.instance and self.instance.pk:
                medicamentos = medicamentos.exclude(pk=self.instance.pk)

            if medicamentos.exists():
                raise ValidationError(
                    'Ya existe un medicamento con este registro sanitario.'
                )

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
            'id_medicamento': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
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
        self.fields['id_medicamento'].required = False  # Puedes hacerlo requerido si quieres
        self.fields['cantidad'].required = False
        self.fields['descuento'].required = False
        self.fields['impuesto'].required = False
    
class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = '__all__'
        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'numero_lote': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: L-2024-001'
            }),
            'fecha_fabricacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Activo, Inactivo'
            }),
            'id_factura_compra': forms.Select(attrs={
                'class': 'form-control'
            }),
            'id_medicamento': forms.Select(attrs={  # NUEVO CAMPO
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Campos que no son obligatorios
        self.fields['fecha_fabricacion'].required = False
        self.fields['fecha_vencimiento'].required = False
        self.fields['estado'].required = False
        self.fields['id_factura_compra'].required = False
        self.fields['id_medicamento'].required = False  # NUEVO

    # =============================
    # VALIDACIONES PERSONALIZADAS
    # =============================

    def clean_numero_lote(self):
        numero_lote = self.cleaned_data.get('numero_lote')

        if numero_lote:
            lotes = Lote.objects.filter(numero_lote=numero_lote)

            # Si estamos editando, excluir el registro actual
            if self.instance and self.instance.pk:
                lotes = lotes.exclude(pk=self.instance.pk)

            if lotes.exists():
                raise ValidationError('Ya existe un lote con este número de lote.')

        return numero_lote

    def clean(self):
        cleaned_data = super().clean()

        fecha_fabricacion = cleaned_data.get('fecha_fabricacion')
        fecha_vencimiento = cleaned_data.get('fecha_vencimiento')

        # Validación lógica de fechas
        if fecha_fabricacion and fecha_vencimiento:
            if fecha_fabricacion > fecha_vencimiento:
                raise ValidationError(
                    "La fecha de fabricación no puede ser mayor a la fecha de vencimiento."
                )

        return cleaned_data
    
class FacturaCompraForm(forms.ModelForm):
    class Meta:
        model = FacturaCompra
        fields = '__all__'

        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'total': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'id_proveedor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'numero_factura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: FAC-2024-001'
            }),
            'impuesto': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Activa, Anulada'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campos opcionales
        self.fields['numero_factura'].required = False
        self.fields['impuesto'].required = False
        self.fields['estado'].required = False

    # =============================
    # VALIDACIONES PERSONALIZADAS
    # =============================
    
    def clean_numero_factura(self):
        numero_factura = self.cleaned_data.get('numero_factura')

        if numero_factura:
            facturas = FacturaCompra.objects.filter(numero_factura=numero_factura)

            # Excluir este registro si estamos editando
            if self.instance and self.instance.pk:
                facturas = facturas.exclude(pk=self.instance.pk)

            if facturas.exists():
                raise ValidationError("Ya existe una factura con este número.")

        return numero_factura

    def clean(self):
        cleaned_data = super().clean()

        total = cleaned_data.get('total')
        impuesto = cleaned_data.get('impuesto')

        # No permitir valores negativos
        if total is not None and total < 0:
            raise ValidationError("El total no puede ser negativo.")

        if impuesto is not None and impuesto < 0:
            raise ValidationError("El impuesto no puede ser negativo.")

        return cleaned_data
    
class LoteMedicamentoForm(forms.ModelForm):
    class Meta:
        model = LoteMedicamento
        fields = '__all__'

        widgets = {
            'id_lote': forms.Select(attrs={
                'class': 'form-control'
            }),
            'id_medicamento': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Cantidad asignada'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    # ===========================================
    # CAMPOS OPCIONALES
    # ===========================================
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['fecha_ingreso'].required = False

    # ===========================================
    # VALIDACIÓN: Cantidad no negativa
    # ===========================================
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')

        if cantidad is not None and cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a cero.")

        return cantidad

    # ===========================================
    # VALIDACIÓN INDIVIDUAL: evitar duplicados (mismo lote + medicamento)
    # ===========================================
    def clean(self):
        cleaned_data = super().clean()

        lote = cleaned_data.get('id_lote')
        medicamento = cleaned_data.get('id_medicamento')

        if lote and medicamento:
            consulta = LoteMedicamento.objects.filter(
                id_lote=lote,
                id_medicamento=medicamento
            )

            # Si está editando, excluir el actual
            if self.instance and self.instance.pk:
                consulta = consulta.exclude(pk=self.instance.pk)

            if consulta.exists():
                raise ValidationError(
                    "Este medicamento ya está asignado a este lote."
                )

        # Validación: fecha de ingreso no puede ser futura
        fecha_ingreso = cleaned_data.get('fecha_ingreso')
        from datetime import date

        if fecha_ingreso and fecha_ingreso > date.today():
            raise ValidationError("La fecha de ingreso no puede ser en el futuro.")

        return cleaned_data
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'fecha_registro': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer todos los campos opcionales excepto nombre si quieres
        self.fields['fecha_registro'].required = False
        self.fields['cedula'].required = False
        self.fields['correo'].required = False
        self.fields['direccion'].required = False
        self.fields['telefono'].required = False

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        # Si la cédula está vacía, está bien
        if not cedula:
            return cedula
            
        # Limpiar espacios
        cedula = cedula.strip()
        
        # Validación más flexible - permitir letras, números, guiones y espacios
        import re
        if not re.match(r'^[A-Za-z0-9\-\.\s]+$', cedula):
            raise ValidationError("La cédula solo puede contener letras, números, guiones, puntos y espacios.")
        
        return cedula

    def clean_fecha_registro(self):
        fecha = self.cleaned_data.get('fecha_registro')
        if fecha and fecha > date.today():
            raise ValidationError("La fecha no puede ser futura.")
        return fecha
class DevolucionClienteForm(forms.ModelForm):
    class Meta:
        model = DevolucionCliente
        fields = [
            'motivo_devolucion',
            'cantidad_devuelta',
            'precio_devolucion',
            'id_venta',
            'id_medicamento',
            'id_empleado',
            'fecha',
            'estado'
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'motivo_devolucion': forms.Textarea(attrs={'rows': 3}),
        }

class DevolucionProveedorForm(forms.ModelForm):
    class Meta:
        model = DevolucionProveedor
        fields = [
            'id_factura_compra',
            'productos_devueltos',
            'cantidad_devuelta',
            'fecha_aprobacion',
            'fecha_registro',
            'estado',
            'id_empleado',
        ]
        widgets = {
            'fecha_aprobacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
            'productos_devueltos': forms.Textarea(attrs={'rows': 3}),
        } 
