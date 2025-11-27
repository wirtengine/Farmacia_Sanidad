from django.db import models
from django.utils import timezone

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_contacto = models.CharField(max_length=255)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateField(blank=True, null=True)
    ruc = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    estado = models.IntegerField(default=1)
    tipo_proveedor = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Proveedor'

    def __str__(self):
        return self.nombre_contacto


class FacturaCompra(models.Model):
    id_factura_compra = models.AutoField(primary_key=True)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=12, decimal_places=2)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, db_column='id_proveedor')
    numero_factura = models.CharField(max_length=50, blank=True, null=True)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Factura_Compra'

    def __str__(self):
        return f"Factura {self.numero_factura}"


class Medicamento(models.Model):

    ESTADOS = [
        (1, 'Activo'),
        (0, 'Inactivo'),
    ]

    id_medicamento = models.AutoField(primary_key=True)
    id_factura_compra = models.ForeignKey(
        FacturaCompra,
        on_delete=models.SET_NULL,
        db_column='id_factura_compra',
        blank=True,
        null=True
    )
    nombre_generico = models.CharField(max_length=255)
    fecha_caducidad = models.DateField(blank=True, null=True)
    cantidad = models.IntegerField(default=0)
    contra_indicaciones = models.TextField(blank=True, null=True)
    dosis = models.CharField(max_length=100, blank=True, null=True)
    cod_laboratorio = models.CharField(max_length=50, blank=True, null=True)
    registro_sanitario = models.CharField(max_length=100, blank=True, null=True)
    precauciones = models.TextField(blank=True, null=True)
    presentacion = models.CharField(max_length=100, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_minimo = models.IntegerField(default=10)
    via_administracion = models.CharField(max_length=100, blank=True, null=True)
    requiere_receta = models.BooleanField(default=False)

    
    estado = models.IntegerField(choices=ESTADOS, default=1)

    fecha_registro = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Medicamento'

    def __str__(self):
        return self.nombre_generico


class Lote(models.Model):
    id_lote = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    numero_lote = models.CharField(max_length=100)
    fecha_fabricacion = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    id_factura_compra = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE, db_column='id_factura_compra', blank=True, null=True)
    
    # AGREGAR ESTA RELACIÓN
    id_medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, db_column='id_medicamento', blank=True, null=True)

    class Meta:
        db_table = 'Lote'

    def __str__(self):
        return f"Lote {self.numero_lote}"


class LoteMedicamento(models.Model):
    id_lote_medicamento = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey(Lote, on_delete=models.CASCADE, db_column='id_lote')
    id_medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, db_column='id_medicamento')
    cantidad = models.IntegerField()
    fecha_ingreso = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Lote_Medicamento'

    def __str__(self):
        return f"LoteMed {self.id_lote_medicamento}"


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    cedula = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    fecha_registro = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Cliente'

    def __str__(self):
        return self.nombre or f"Cliente {self.id_cliente}"


class Empleados(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    fecha_contratacion = models.DateField(blank=True, null=True)
    rol = models.CharField(max_length=100, blank=True, null=True)
    funciones = models.TextField(blank=True, null=True)
    cedula = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = 'Empleados'

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, db_column='id_cliente', blank=True, null=True)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.SET_NULL, db_column='id_empleado', blank=True, null=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    
    # Agregar estos dos campos
    id_medicamento = models.ForeignKey(Medicamento, on_delete=models.SET_NULL, blank=True, null=True)
    cantidad = models.IntegerField(default=1)

    class Meta:
        db_table = 'Venta'

    def __str__(self):
        return f"Venta {self.id_venta}"


class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    id_medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, db_column='id_medicamento', blank=True, null=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, db_column='id_venta', blank=True, null=True)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Factura'

    def __str__(self):
        return f"Factura {self.id_factura}"


class MetodoPago(models.Model):
    id_metodo_pago = models.AutoField(primary_key=True)
    tipo_pago = models.CharField(max_length=50, blank=True, null=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, db_column='id_venta', blank=True, null=True)
    referencia_pago = models.CharField(max_length=100, blank=True, null=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'Metodo_Pago'

    def __str__(self):
        return f"{self.tipo_pago} - {self.monto}"


class CompraMedicamento(models.Model):
    id_compra_medicamento = models.AutoField(primary_key=True)
    id_factura_compra = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE, db_column='id_factura_compra')
    id_medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, db_column='id_medicamento')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'Compra_Medicamento'

    def __str__(self):
        return f"CompraMed {self.id_compra_medicamento}"


class DevolucionCliente(models.Model):
    id_devolucion_cliente = models.AutoField(primary_key=True)
    motivo_devolucion = models.TextField(blank=True, null=True)
    cantidad_devuelta = models.IntegerField(blank=True, null=True)
    precio_devolucion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, db_column='id_venta', blank=True, null=True)
    id_medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, db_column='id_medicamento', blank=True, null=True)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, db_column='id_empleado', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Devolucion_Cliente'

    def __str__(self):
        return f"Devolución {self.id_devolucion_cliente}"


class DevolucionProveedor(models.Model):
    id_devolucion = models.AutoField(primary_key=True)
    id_factura_compra = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE, db_column='id_factura_compra', blank=True, null=True)
    productos_devueltos = models.TextField(blank=True, null=True)
    cantidad_devuelta = models.IntegerField(blank=True, null=True)
    fecha_aprobacion = models.DateField(blank=True, null=True)
    fecha_registro = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, db_column='id_empleado', blank=True, null=True)

    class Meta:
        db_table = 'Devolucion_Proveedor'

    def __str__(self):
        return f"Devolución Prov {self.id_devolucion}"


class EstadoCompra(models.Model):
    id_estado_compra = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    id_compra = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE, db_column='id_compra', blank=True, null=True)

    class Meta:
        db_table = 'Estado_Compra'

    def __str__(self):
        return f"Estado Compra {self.id_estado_compra}"


class EstadoDevolucionProveedor(models.Model):
    id_estado_devolucion = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    id_devolucion = models.ForeignKey(DevolucionProveedor, on_delete=models.CASCADE, db_column='id_devolucion', blank=True, null=True)

    class Meta:
        db_table = 'Estado_Devolucion_Proveedor'

    def __str__(self):
        return f"Estado Dev {self.id_estado_devolucion}"


class PresentacionMedicamento(models.Model):
    id_presentacion = models.AutoField(primary_key=True)
    tipo_presentacion = models.CharField(max_length=100, blank=True, null=True)
    id_medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, db_column='id_medicamento', blank=True, null=True)

    class Meta:
        db_table = 'Presentacion_Medicamento'

    def __str__(self):
        return f"Presentación {self.tipo_presentacion}"