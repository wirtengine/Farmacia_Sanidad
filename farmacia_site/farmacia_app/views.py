from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicamento, Proveedor, Empleados, Venta
from .forms import MedicamentoForm, ProveedorForm, EmpleadoForm, VentaForm

# ===========================
# VISTA HOME (MENÚ PRINCIPAL)
# ===========================
def home(request):
    return render(request, 'home/home.html')


# ===========================
# VISTAS DE MEDICAMENTOS
# ===========================
def medicamento_list(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'medicamento/list.html', {'medicamentos': medicamentos})

def medicamento_create(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            medicamento = form.save(commit=False)
            # Valores por defecto para evitar errores de la DB
            if not medicamento.nombre_generico:
                medicamento.nombre_generico = 'N/A'
            if medicamento.cantidad is None:
                medicamento.cantidad = 0
            if medicamento.precio_unitario is None:
                medicamento.precio_unitario = 0.0
            medicamento.save()
            return redirect('medicamento_list')
    else:
        form = MedicamentoForm()
    return render(request, 'medicamento/create.html', {'form': form})

# EDITAR
def medicamento_edit(request, id_medicamento):
    medicamento = get_object_or_404(Medicamento, pk=id_medicamento)
    form = MedicamentoForm(request.POST or None, instance=medicamento)
    if form.is_valid():
        medicamento = form.save(commit=False)
        # Valores por defecto para evitar errores de la DB
        if not medicamento.nombre_generico:
            medicamento.nombre_generico = 'N/A'
        if medicamento.cantidad is None:
            medicamento.cantidad = 0
        if medicamento.precio_unitario is None:
            medicamento.precio_unitario = 0.0
        medicamento.save()
        return redirect('medicamento_list')
    return render(request, 'medicamento/edit.html', {'form': form})

# ELIMINAR
def medicamento_delete(request, id_medicamento):
    medicamento = get_object_or_404(Medicamento, pk=id_medicamento)
    medicamento.delete()
    return redirect('medicamento_list')

def medicamento_edit(request, id_medicamento):
    medicamento = get_object_or_404(Medicamento, pk=id_medicamento)
    
    # Debug: mostrar información del medicamento
    print(f"=== EDITANDO MEDICAMENTO ID: {id_medicamento} ===")
    print(f"Nombre: {medicamento.nombre_generico}")
    print(f"Cantidad: {medicamento.cantidad}")
    print(f"Precio: {medicamento.precio_unitario}")
    print(f"Estado: {medicamento.estado}")
    
    if request.method == 'POST':
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
                
                # Valores por defecto para evitar errores
                if not medicamento_actualizado.nombre_generico:
                    medicamento_actualizado.nombre_generico = 'N/A'
                if medicamento_actualizado.cantidad is None:
                    medicamento_actualizado.cantidad = 0
                if medicamento_actualizado.precio_unitario is None:
                    medicamento_actualizado.precio_unitario = 0.0
                
                medicamento_actualizado.save()
                print("=== MEDICAMENTO ACTUALIZADO ===")
                return redirect('medicamento_list')
            except Exception as e:
                print(f"=== ERROR AL GUARDAR ===")
                print(f"Error: {str(e)}")
        else:
            print("=== ERRORES DEL FORMULARIO ===")
            print(form.errors)
    else:
        # GET request - mostrar formulario con datos existentes
        form = MedicamentoForm(instance=medicamento)
        print("=== FORMULARIO CARGADO (GET) ===")
        print(f"Valores iniciales del formulario: {form.initial}")
    
    return render(request, 'medicamento/edit.html', {
        'form': form,
        'medicamento': medicamento
    })


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
            form.save()
            return redirect('venta_list')
    else:
        form = VentaForm()
    return render(request, 'venta/create.html', {'form': form})

def venta_edit(request, id_venta):
    venta = get_object_or_404(Venta, pk=id_venta)
    form = VentaForm(request.POST or None, instance=venta)
    if form.is_valid():
        form.save()
        return redirect('venta_list')
    return render(request, 'venta/edit.html', {'form': form})

def venta_delete(request, id_venta):
    venta = get_object_or_404(Venta, pk=id_venta)
    venta.delete()
    return redirect('venta_list')
