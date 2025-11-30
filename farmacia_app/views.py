from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required  
from .models import Medicamento, Proveedor, Empleados, Venta, Lote, FacturaCompra, LoteMedicamento, Cliente, DevolucionCliente,DevolucionProveedor
from .forms import MedicamentoForm, ProveedorForm, EmpleadoForm, VentaForm, LoteForm,FacturaCompraForm, LoteMedicamentoForm, ClienteForm,DevolucionClienteForm,DevolucionProveedorForm


# ===========================
# VISTA HOME (MENÚ PRINCIPAL)
# ===========================
@login_required
def home(request):
    """
    Vista principal que muestra contenido diferente según el rol del usuario
    """
    # Obtener el rol del usuario actual
    rol_usuario = request.user.rol
    
    # Pasar el rol al contexto del template
    context = {
        'rol': rol_usuario
    }
    
    return render(request, 'home/home.html', context)


# ===========================
# VISTAS DE MEDICAMENTOS
# ===========================
@login_required
def medicamento_list(request):
    """
    Vista para listar todos los medicamentos
    """
    try:
        medicamentos = Medicamento.objects.all().order_by('nombre_generico')
        
        # Filtros opcionales
        estado_filter = request.GET.get('estado')
        if estado_filter:
            medicamentos = medicamentos.filter(estado=int(estado_filter))
        
        search_query = request.GET.get('search')
        if search_query:
            medicamentos = medicamentos.filter(nombre_generico__icontains=search_query)
        
        context = {
            'medicamentos': medicamentos,
            'total_medicamentos': medicamentos.count(),
            'medicamentos_activos': medicamentos.filter(estado=1).count(),
            'medicamentos_inactivos': medicamentos.filter(estado=0).count(),
        }
        
        return render(request, 'medicamento/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar la lista de medicamentos: {str(e)}')
        return render(request, 'medicamento/list.html', {'medicamentos': []})

@login_required
def medicamento_create(request):
    """
    Vista para crear un nuevo medicamento
    """
    # Opciones para los select
    presentation_choices = [
        ('Tabletas', 'Tabletas'),
        ('Cápsulas', 'Cápsulas'), 
        ('Jarabe', 'Jarabe'),
        ('Inyectable', 'Inyectable'),
        ('Crema', 'Crema'),
        ('Ungüento', 'Ungüento'),
        ('Supositorio', 'Supositorio'),
        ('Inhalador', 'Inhalador'),
        ('Suspensión', 'Suspensión'),
        ('Polvo', 'Polvo'),
        ('Granulado', 'Granulado'),
        ('Spray', 'Spray'),
        ('Gel', 'Gel'),
        ('Parche', 'Parche'),
        ('Implante', 'Implante'),
        ('Solución', 'Solución'),
    ]
    
    via_choices = [
        ('Oral', 'Oral'),
        ('Intramuscular', 'Intramuscular'),
        ('Intravenosa', 'Intravenosa'),
        ('Subcutánea', 'Subcutánea'),
        ('Tópica', 'Tópica'),
        ('Oftálmica', 'Oftálmica'),
        ('Ótica', 'Ótica'),
        ('Nasal', 'Nasal'),
        ('Inhalatoria', 'Inhalatoria'),
        ('Rectal', 'Rectal'),
        ('Vaginal', 'Vaginal'),
        ('Transdérmica', 'Transdérmica'),
        ('Sublingual', 'Sublingual'),
        ('Bucal', 'Bucal'),
    ]

    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            try:
                medicamento = form.save(commit=False)
                
                # Valores por defecto para evitar errores de la DB
                if not medicamento.nombre_generico:
                    medicamento.nombre_generico = 'N/A'
                if medicamento.cantidad is None:
                    medicamento.cantidad = 0
                if medicamento.precio_unitario is None:
                    medicamento.precio_unitario = 0.0
                # stock_minimo ya se maneja en el clean_stock_minimo del formulario
                
                medicamento.save()
                messages.success(request, f'Medicamento "{medicamento.nombre_generico}" creado exitosamente.')
                return redirect('medicamento_list')
                
            except Exception as e:
                messages.error(request, f'Error al guardar el medicamento: {str(e)}')
                print(f"Error al crear medicamento: {str(e)}")
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
            print("Errores del formulario:", form.errors)
    else:
        form = MedicamentoForm()
    
    context = {
        'form': form,
        'presentation_choices': presentation_choices,
        'via_choices': via_choices,
        'accion': 'crear'
    }
    
    return render(request, 'medicamento/create.html', context)

@login_required
def medicamento_edit(request, id_medicamento):
    """
    Vista para editar un medicamento existente
    """
    medicamento = get_object_or_404(Medicamento, pk=id_medicamento)
    
    # Opciones para los select
    presentation_choices = [
        ('Tabletas', 'Tabletas'),
        ('Cápsulas', 'Cápsulas'),
        ('Jarabe', 'Jarabe'),
        ('Inyectable', 'Inyectable'),
        ('Crema', 'Crema'),
        ('Ungüento', 'Ungüento'),
        ('Supositorio', 'Supositorio'),
        ('Inhalador', 'Inhalador'),
        ('Suspensión', 'Suspensión'),
        ('Polvo', 'Polvo'),
        ('Granulado', 'Granulado'),
        ('Spray', 'Spray'),
        ('Gel', 'Gel'),
        ('Parche', 'Parche'),
        ('Implante', 'Implante'),
        ('Solución', 'Solución'),
    ]
    
    via_choices = [
        ('Oral', 'Oral'),
        ('Intramuscular', 'Intramuscular'),
        ('Intravenosa', 'Intravenosa'),
        ('Subcutánea', 'Subcutánea'),
        ('Tópica', 'Tópica'),
        ('Oftálmica', 'Oftálmica'),
        ('Ótica', 'Ótica'),
        ('Nasal', 'Nasal'),
        ('Inhalatoria', 'Inhalatoria'),
        ('Rectal', 'Rectal'),
        ('Vaginal', 'Vaginal'),
        ('Transdérmica', 'Transdérmica'),
        ('Sublingual', 'Sublingual'),
        ('Bucal', 'Bucal'),
    ]

    if request.method == 'POST':
        print(f"=== EDITANDO MEDICAMENTO ID: {id_medicamento} ===")
        print(f"Nombre actual: {medicamento.nombre_generico}")
        print(f"Cantidad actual: {medicamento.cantidad}")
        print(f"Precio actual: {medicamento.precio_unitario}")
        print(f"Estado actual: {medicamento.estado}")
        print(f"Stock mínimo actual: {medicamento.stock_minimo}")
        
        print("=== DATOS DEL FORMULARIO (POST) ===")
        for key, value in request.POST.items():
            print(f"{key}: {value}")
        
        form = MedicamentoForm(request.POST, instance=medicamento)
        print(f"Formulario válido: {form.is_valid()}")
        
        if form.is_valid():
            try:
                medicamento_actualizado = form.save(commit=False)
                print("=== ANTES DE GUARDAR ===")
                print(f"Nombre: {medicamento_actualizado.nombre_generico}")
                print(f"Cantidad: {medicamento_actualizado.cantidad}")
                print(f"Precio: {medicamento_actualizado.precio_unitario}")
                print(f"Stock mínimo: {medicamento_actualizado.stock_minimo}")
                print(f"Estado: {medicamento_actualizado.estado}")
                
                # Valores por defecto para evitar errores
                if not medicamento_actualizado.nombre_generico:
                    medicamento_actualizado.nombre_generico = 'N/A'
                if medicamento_actualizado.cantidad is None:
                    medicamento_actualizado.cantidad = 0
                if medicamento_actualizado.precio_unitario is None:
                    medicamento_actualizado.precio_unitario = 0.0
                # stock_minimo ya se maneja en el clean_stock_minimo del formulario
                
                medicamento_actualizado.save()
                print("=== MEDICAMENTO ACTUALIZADO ===")
                messages.success(request, f'Medicamento "{medicamento_actualizado.nombre_generico}" actualizado exitosamente.')
                return redirect('medicamento_list')
                
            except Exception as e:
                print(f"=== ERROR AL GUARDAR ===")
                print(f"Error: {str(e)}")
                messages.error(request, f'Error al actualizar el medicamento: {str(e)}')
        else:
            print("=== ERRORES DEL FORMULARIO ===")
            print(form.errors)
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        # GET request - mostrar formulario con datos existentes
        form = MedicamentoForm(instance=medicamento)
        print("=== FORMULARIO CARGADO (GET) ===")
        print(f"Valores iniciales del formulario: {form.initial}")
    
    context = {
        'form': form,
        'medicamento': medicamento,
        'presentation_choices': presentation_choices,
        'via_choices': via_choices,
        'accion': 'editar'
    }
    
    return render(request, 'medicamento/create.html', context)

@login_required
def medicamento_delete(request, id_medicamento):
    """
    Vista para eliminar un medicamento
    """
    medicamento = get_object_or_404(Medicamento, pk=id_medicamento)
    
    if request.method == 'POST':
        try:
            nombre_medicamento = medicamento.nombre_generico
            medicamento.delete()
            messages.success(request, f'Medicamento "{nombre_medicamento}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el medicamento: {str(e)}')
        
        return redirect('medicamento_list')
    
    # Si es GET, mostrar página de confirmación
    return render(request, 'medicamento/confirm_delete.html', {'medicamento': medicamento})

@login_required
def medicamento_detail(request, id_medicamento):
    """
    Vista para ver los detalles de un medicamento
    """
    medicamento = get_object_or_404(Medicamento, pk=id_medicamento)
    
    # Calcular estado del stock
    estado_stock = 'Normal'
    if medicamento.cantidad <= 0:
        estado_stock = 'Agotado'
    elif medicamento.cantidad <= medicamento.stock_minimo:
        estado_stock = 'Bajo Stock'
    
    context = {
        'medicamento': medicamento,
        'estado_stock': estado_stock,
    }
    
    return render(request, 'medicamento/detail.html', context)

@login_required
def medicamento_toggle_estado(request, id_medicamento):
    """
    Vista para cambiar el estado de un medicamento (Activo/Inactivo)
    """
    medicamento = get_object_or_404(Medicamento, pk=id_medicamento)
    
    try:
        # Cambiar estado
        nuevo_estado = 0 if medicamento.estado == 1 else 1
        medicamento.estado = nuevo_estado
        medicamento.save()
        
        estado_texto = 'activado' if nuevo_estado == 1 else 'desactivado'
        messages.success(request, f'Medicamento "{medicamento.nombre_generico}" {estado_texto} exitosamente.')
        
    except Exception as e:
        messages.error(request, f'Error al cambiar el estado del medicamento: {str(e)}')
    
    return redirect('medicamento_list')

@login_required
def medicamento_stock_report(request):
    """
    Vista para generar reporte de stock
    """
    try:
        medicamentos = Medicamento.objects.all().order_by('nombre_generico')
        
        # Categorizar medicamentos por estado de stock
        medicamentos_agotados = medicamentos.filter(cantidad=0)
        medicamentos_bajo_stock = medicamentos.filter(cantidad__gt=0, cantidad__lte=models.F('stock_minimo'))
        medicamentos_stock_normal = medicamentos.filter(cantidad__gt=models.F('stock_minimo'))
        
        # Estadísticas
        total_valor_inventario = sum(
            med.cantidad * (med.precio_unitario or 0) 
            for med in medicamentos 
            if med.precio_unitario is not None
        )
        
        context = {
            'medicamentos_agotados': medicamentos_agotados,
            'medicamentos_bajo_stock': medicamentos_bajo_stock,
            'medicamentos_stock_normal': medicamentos_stock_normal,
            'total_medicamentos': medicamentos.count(),
            'total_valor_inventario': total_valor_inventario,
            'total_agotados': medicamentos_agotados.count(),
            'total_bajo_stock': medicamentos_bajo_stock.count(),
        }
        
        return render(request, 'medicamento/stock_report.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al generar el reporte de stock: {str(e)}')
        return render(request, 'medicamento/stock_report.html', {})

# ===========================
# VISTAS DE PROVEEDORES
# ===========================
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedor/list.html', {'proveedores': proveedores})

def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'proveedor/create.html', {'form': form})

def proveedor_edit(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, pk=id_proveedor)
    form = ProveedorForm(request.POST or None, instance=proveedor)
    if form.is_valid():
        form.save()
        return redirect('proveedor_list')
    return render(request, 'proveedor/edit.html', {'form': form})

def proveedor_delete(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, pk=id_proveedor)
    proveedor.delete()
    return redirect('proveedor_list')

def proveedor_edit(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, pk=id_proveedor)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedor/edit.html', {'form': form, 'proveedor': proveedor})
# ===========================
# VISTAS DE EMPLEADOS
# ===========================
def empleado_list(request):
    empleados = Empleados.objects.all()
    return render(request, 'empleado/list.html', {'empleados': empleados})

def empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'empleado/create.html', {'form': form})

def empleado_edit(request, id_empleado):
    empleado = get_object_or_404(Empleados, pk=id_empleado)
    form = EmpleadoForm(request.POST or None, instance=empleado)
    if form.is_valid():
        form.save()
        return redirect('empleado_list')
    return render(request, 'empleado/edit.html', {'form': form})

def empleado_delete(request, id_empleado):
    empleado = get_object_or_404(Empleados, pk=id_empleado)
    empleado.delete()
    return redirect('empleado_list')


# ===========================
# VISTAS DE VENTAS
# ===========================
def venta_list(request):
    ventas = Venta.objects.all()
    return render(request, 'venta/list.html', {'ventas': ventas})

def venta_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            # Guardar la venta primero
            venta = form.save(commit=False)
            
            # Verificar que hay suficiente stock
            medicamento = venta.id_medicamento
            if venta.cantidad > medicamento.cantidad:
                # Si no hay suficiente stock, mostrar error
                form.add_error('cantidad', f'No hay suficiente stock. Stock disponible: {medicamento.cantidad}')
            else:
                # Si hay stock, guardar la venta y actualizar stock
                venta.save()
                medicamento.cantidad -= venta.cantidad
                medicamento.save()
                return redirect('venta_list')
    else:
        form = VentaForm()
    
    # Obtener clientes, empleados y medicamentos para los selects
    clientes = Cliente.objects.all()
    empleados = Empleados.objects.all()
    medicamentos = Medicamento.objects.filter(cantidad__gt=0)  # Solo medicamentos con stock
    
    return render(request, 'venta/create.html', {
        'form': form,
        'clientes': clientes,
        'empleados': empleados,
        'medicamentos': medicamentos
    })

def venta_edit(request, id_venta):
    venta = get_object_or_404(Venta, pk=id_venta)
    cantidad_original = venta.cantidad
    medicamento_original = venta.id_medicamento
    
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            venta_nueva = form.save(commit=False)
            medicamento_nuevo = venta_nueva.id_medicamento
            
            # Caso 1: Mismo medicamento, cambiar cantidad
            if medicamento_original == medicamento_nuevo:
                diferencia = venta_nueva.cantidad - cantidad_original
                if diferencia > medicamento_original.cantidad:
                    form.add_error('cantidad', f'No hay suficiente stock. Stock disponible: {medicamento_original.cantidad}')
                else:
                    medicamento_original.cantidad -= diferencia
                    medicamento_original.save()
                    venta_nueva.save()
                    return redirect('venta_list')
            
            # Caso 2: Diferente medicamento
            else:
                # Verificar stock en el nuevo medicamento
                if venta_nueva.cantidad > medicamento_nuevo.cantidad:
                    form.add_error('cantidad', f'No hay suficiente stock en el nuevo medicamento. Stock disponible: {medicamento_nuevo.cantidad}')
                else:
                    # Restaurar stock del medicamento original
                    medicamento_original.cantidad += cantidad_original
                    medicamento_original.save()
                    
                    # Descontar stock del nuevo medicamento
                    medicamento_nuevo.cantidad -= venta_nueva.cantidad
                    medicamento_nuevo.save()
                    
                    venta_nueva.save()
                    return redirect('venta_list')
    else:
        form = VentaForm(instance=venta)
    
    # Obtener clientes, empleados y medicamentos para los selects
    clientes = Cliente.objects.all()
    empleados = Empleados.objects.all()
    medicamentos = Medicamento.objects.filter(cantidad__gt=0)
    
    return render(request, 'venta/edit.html', {
        'form': form,
        'venta': venta,
        'clientes': clientes,
        'empleados': empleados,
        'medicamentos': medicamentos
    })

def venta_delete(request, id_venta):
    venta = get_object_or_404(Venta, pk=id_venta)
    
    # Restaurar el stock del medicamento antes de eliminar la venta
    medicamento = venta.id_medicamento
    medicamento.cantidad += venta.cantidad
    medicamento.save()
    
    venta.delete()
    return redirect('venta_list')

def lote_list(request):
    lotes = Lote.objects.all()
    return render(request, 'lote/list.html', {'lotes': lotes})


def lote_create(request):
    if request.method == 'POST':
        form = LoteForm(request.POST)

        print("=== DATOS DEL FORMULARIO (POST) ===")
        for key, value in request.POST.items():
            print(f"{key}: {value}")

        if form.is_valid():
            lote = form.save(commit=False)

            # Validaciones básicas para evitar errores
            if lote.cantidad is None:
                lote.cantidad = 0
            if not lote.numero_lote:
                lote.numero_lote = "SIN-LOTE"
            if not lote.estado:
                lote.estado = "DESCONOCIDO"

            lote.save()
            return redirect('lote_list')
        else:
            print("=== ERRORES DEL FORMULARIO ===")
            print(form.errors)

    else:
        form = LoteForm()

    # OBTENER MEDICAMENTOS PARA EL CONTEXTO
    medicamentos = Medicamento.objects.all()
    
    return render(request, 'lote/create.html', {
        'form': form,
        'medicamentos': medicamentos  # Añadir al contexto
    })


def lote_edit(request, id_lote):
    lote = get_object_or_404(Lote, pk=id_lote)

    print(f"=== EDITANDO LOTE ID: {id_lote} ===")
    print(f"Número lote: {lote.numero_lote}")
    print(f"Cantidad: {lote.cantidad}")
    print(f"Estado: {lote.estado}")

    if request.method == 'POST':
        form = LoteForm(request.POST, instance=lote)

        print("=== DATOS DEL FORMULARIO (POST) ===")
        for key, value in request.POST.items():
            print(f"{key}: {value}")

        if form.is_valid():
            lote_actualizado = form.save(commit=False)

            if lote_actualizado.cantidad is None:
                lote_actualizado.cantidad = 0
            if not lote_actualizado.numero_lote:
                lote_actualizado.numero_lote = "SIN-LOTE"
            if not lote_actualizado.estado:
                lote_actualizado.estado = "DESCONOCIDO"

            lote_actualizado.save()
            return redirect('lote_list')

        else:
            print("=== ERRORES DEL FORMULARIO ===")
            print(form.errors)

    else:
        form = LoteForm(instance=lote)
        print("=== FORMULARIO CARGADO (GET) ===")

    # OBTENER MEDICAMENTOS PARA EL CONTEXTO
    medicamentos = Medicamento.objects.all()

    return render(request, 'lote/edit.html', {
        'form': form,
        'lote': lote,
        'medicamentos': medicamentos  # Añadir al contexto
    })


def lote_delete(request, id_lote):
    lote = get_object_or_404(Lote, pk=id_lote)
    lote.delete()
    return redirect('lote_list')

# LISTAR FACTURAS
def facturacompra_list(request):
    facturas = FacturaCompra.objects.all()
    return render(request, 'facturas/facturacompra_list.html', {'facturas': facturas})


# CREAR FACTURA
def facturacompra_create(request):
    if request.method == 'POST':
        form = FacturaCompraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facturacompra_list')
    else:
        form = FacturaCompraForm()

    # OBTENER PROVEEDORES PARA EL CONTEXTO
    proveedores = Proveedor.objects.all()
    
    return render(request, 'facturas/facturacompra_form.html', {
        'form': form, 
        'titulo': 'Crear Factura de Compra',
        'proveedores': proveedores  # Añadir al contexto
    })


# EDITAR FACTURA
def facturacompra_edit(request, id_factura_compra):
    factura = get_object_or_404(FacturaCompra, id_factura_compra=id_factura_compra)

    if request.method == 'POST':
        form = FacturaCompraForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            return redirect('facturacompra_list')
    else:
        form = FacturaCompraForm(instance=factura)

    # OBTENER PROVEEDORES PARA EL CONTEXTO
    proveedores = Proveedor.objects.all()

    return render(request, 'facturas/facturacompra_form.html', {
        'form': form, 
        'titulo': 'Editar Factura de Compra',
        'factura': factura,
        'proveedores': proveedores  # Añadir al contexto
    })


# ELIMINAR FACTURA
def facturacompra_delete(request, id_factura_compra):
    factura = get_object_or_404(FacturaCompra, id_factura_compra=id_factura_compra)

    if request.method == 'POST':
        factura.delete()
        return redirect('facturacompra_list')

    return render(request, 'facturas/facturacompra_delete.html', {'factura': factura})

# LISTAR LOTES DE MEDICAMENTOS
def lotemedicamento_list(request):
    lotes = LoteMedicamento.objects.all()
    return render(request, 'lotemedicamento/list.html', {'lotes': lotes})


# CREAR LOTE
def lotemedicamento_create(request):
    if request.method == 'POST':
        form = LoteMedicamentoForm(request.POST)
        if form.is_valid():

            lote = form.save(commit=False)

            # Validación simple
            if lote.cantidad is None:
                lote.cantidad = 0

            lote.save()
            return redirect('lotemedicamento_list')

    else:
        form = LoteMedicamentoForm()

    return render(request, 'lotemedicamento/form.html', {
        'form': form,
        'titulo': 'Asignar Medicamento a Lote'
    })


# EDITAR LOTE
def lotemedicamento_edit(request, id_lote_medicamento):
    lote_med = get_object_or_404(LoteMedicamento, pk=id_lote_medicamento)

    if request.method == 'POST':
        form = LoteMedicamentoForm(request.POST, instance=lote_med)
        if form.is_valid():
            form.save()
            return redirect('lotemedicamento_list')

    else:
        form = LoteMedicamentoForm(instance=lote_med)

    return render(request, 'lotemedicamento/form.html', {
        'form': form,
        'titulo': 'Editar Lote de Medicamento'
    })


# ELIMINAR LOTE
def lotemedicamento_delete(request, id_lote_medicamento):
    lote_med = get_object_or_404(LoteMedicamento, pk=id_lote_medicamento)

    if request.method == 'POST':
        lote_med.delete()
        return redirect('lotemedicamento_list')

    return render(request, 'lotemedicamento/delete.html', {'lote': lote_med})

def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/cliente_list.html', {'clientes': clientes})

# ===========================
# CREAR CLIENTE
# ===========================
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/cliente_list.html', {'clientes': clientes})

# ===========================
# CREAR CLIENTE
# ===========================
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                # Guardar el formulario
                form.save()
                messages.success(request, "Cliente registrado exitosamente.")
                return redirect('cliente_list')
            except Exception as e:
                messages.error(request, f"Error al guardar: {str(e)}")
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ClienteForm()
    
    return render(request, 'cliente/cliente_form.html', {'form': form, 'titulo': 'Nuevo Cliente'})

# ===========================
# EDITAR CLIENTE
# ===========================
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Cliente actualizado correctamente.")
                return redirect('cliente_list')
            except Exception as e:
                messages.error(request, f"Error al guardar: {str(e)}")
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'cliente/cliente_form.html', {'form': form, 'titulo': 'Editar Cliente'})

# ===========================
# ELIMINAR CLIENTE (SOLO BOTÓN - SIN TEMPLATE DE CONFIRMACIÓN)
# ===========================
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        try:
            cliente.delete()
            messages.success(request, "Cliente eliminado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al eliminar: {str(e)}")
    
    # Siempre redirigir a la lista, independientemente del método
    return redirect('cliente_list')

# LISTAR
def devolucioncliente_list(request):
    devoluciones = DevolucionCliente.objects.select_related(
        'id_venta', 'id_medicamento', 'id_empleado'
    ).all().order_by('-id_devolucion_cliente')
    return render(request, 'devolucioncliente/devolucion_list.html', {'devoluciones': devoluciones})

# CREAR
def devolucioncliente_create(request):
    # Obtener las listas para los dropdowns
    ventas = Venta.objects.all()
    medicamentos = Medicamento.objects.all()
    empleados = Empleados.objects.all()
    
    if request.method == 'POST':
        form = DevolucionClienteForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    devolucion = form.save(commit=False)

                    # (Opcional) Cálculo automático de precio total devuelto
                    if devolucion.precio_devolucion and devolucion.cantidad_devuelta:
                        devolucion.precio_devolucion = devolucion.precio_devolucion * devolucion.cantidad_devuelta

                    devolucion.save()

                messages.success(request, "Devolución registrada correctamente.")
                return redirect('devolucion_list')

            except Exception as e:
                messages.error(request, f"Error al registrar la devolución: {e}")
        else:
            messages.error(request, "El formulario tiene errores.")
    else:
        form = DevolucionClienteForm()

    return render(request, 'devolucioncliente/devolucion_form.html', {
        'form': form, 
        'titulo': 'Registrar Devolución',
        'ventas': ventas,
        'medicamentos': medicamentos,
        'empleados': empleados
    })

# EDITAR
def devolucioncliente_edit(request, pk):
    devolucion = get_object_or_404(DevolucionCliente, pk=pk)
    
    # Obtener las listas para los dropdowns
    ventas = Venta.objects.all()
    medicamentos = Medicamento.objects.all()
    empleados = Empleados.objects.all()

    if request.method == 'POST':
        form = DevolucionClienteForm(request.POST, instance=devolucion)

        if form.is_valid():
            try:
                with transaction.atomic():
                    devolucion = form.save(commit=False)

                    if devolucion.precio_devolucion and devolucion.cantidad_devuelta:
                        devolucion.precio_devolucion = devolucion.precio_devolucion * devolucion.cantidad_devuelta

                    devolucion.save()

                messages.success(request, "Devolución actualizada correctamente.")
                return redirect('devolucion_list')

            except Exception as e:
                messages.error(request, f"Error al actualizar la devolución: {e}")

    else:
        form = DevolucionClienteForm(instance=devolucion)

    return render(request, 'devolucioncliente/devolucion_form.html', {
        'form': form, 
        'titulo': 'Editar Devolución',
        'devolucion': devolucion,
        'ventas': ventas,
        'medicamentos': medicamentos,
        'empleados': empleados
    })

# ELIMINAR
def devolucioncliente_delete(request, pk):
    devolucion = get_object_or_404(DevolucionCliente, pk=pk)

    if request.method == 'POST':
        devolucion.delete()
        messages.success(request, "Devolución eliminada correctamente.")
        return redirect('devolucion_list')

    return render(request, 'devolucioncliente/devolucion_delete.html', {'devolucion': devolucion})

# LISTA
def devolucionproveedor_list(request):
    devoluciones = DevolucionProveedor.objects.select_related(
        'id_factura_compra', 'id_empleado'
    ).all().order_by('-id_devolucion')
    return render(request, 'devolucionproveedor/devolucionprov_list.html', {
        'devoluciones': devoluciones
    })


# CREAR
def devolucionproveedor_create(request):
    # Obtener las listas para los dropdowns
    facturas = FacturaCompra.objects.select_related('id_proveedor').all()
    empleados = Empleados.objects.all()
    
    if request.method == 'POST':
        form = DevolucionProveedorForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    devolucion = form.save()
                messages.success(request, "Devolución de proveedor registrada correctamente.")
                return redirect('devolucionprov_list')
            except Exception as e:
                messages.error(request, f"Error al registrar la devolución: {e}")
        else:
            messages.error(request, "El formulario contiene errores.")

    else:
        form = DevolucionProveedorForm()

    return render(request, 'devolucionproveedor/devolucionprov_form.html', {
        'form': form,
        'titulo': 'Registrar Devolución a Proveedor',
        'facturas': facturas,
        'empleados': empleados
    })


# EDITAR
def devolucionproveedor_edit(request, pk):
    devolucion = get_object_or_404(DevolucionProveedor, pk=pk)
    
    # Obtener las listas para los dropdowns
    facturas = FacturaCompra.objects.select_related('id_proveedor').all()
    empleados = Empleados.objects.all()

    if request.method == 'POST':
        form = DevolucionProveedorForm(request.POST, instance=devolucion)

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, "Devolución actualizada correctamente.")
                return redirect('devolucionprov_list')
            except Exception as e:
                messages.error(request, f"Error al actualizar la devolución: {e}")

    else:
        form = DevolucionProveedorForm(instance=devolucion)

    return render(request, 'devolucionproveedor/devolucionprov_form.html', {
        'form': form,
        'titulo': 'Editar Devolución de Proveedor',
        'devolucion': devolucion,
        'facturas': facturas,
        'empleados': empleados
    })


# ELIMINAR
def devolucionproveedor_delete(request, pk):
    devolucion = get_object_or_404(DevolucionProveedor, pk=pk)

    if request.method == 'POST':
        devolucion.delete()
        messages.success(request, "Devolución eliminada correctamente.")
        return redirect('devolucionprov_list')

    return render(request, 'devolucionproveedor/devolucionprov_delete.html', {
        'devolucion': devolucion
    })

