from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Home temporal
    path('home/', login_required(views.home), name='home'),

    # =======================
    # RUTAS DE MEDICAMENTOS
    # =======================
    path('medicamentos/', login_required(views.medicamento_list), name='medicamento_list'),
    path('medicamentos/crear/', login_required(views.medicamento_create), name='medicamento_create'),
    path('medicamentos/editar/<int:id_medicamento>/', login_required(views.medicamento_edit), name='medicamento_edit'),
    path('medicamentos/eliminar/<int:id_medicamento>/', login_required(views.medicamento_delete), name='medicamento_delete'),
    
    # Vistas adicionales
    path('medicamentos/detalle/<int:id_medicamento>/', login_required(views.medicamento_detail), name='medicamento_detail'),
    path('medicamentos/cambiar-estado/<int:id_medicamento>/', login_required(views.medicamento_toggle_estado), name='medicamento_toggle_estado'),
    path('medicamentos/reporte-stock/', login_required(views.medicamento_stock_report), name='medicamento_stock_report'),
    # =======================
    # RUTAS DE PROVEEDORES
    # =======================
    path('proveedores/', login_required(views.proveedor_list), name='proveedor_list'),
    path('proveedores/crear/', login_required(views.proveedor_create), name='proveedor_create'),
    path('proveedores/editar/<int:id_proveedor>/', login_required(views.proveedor_edit), name='proveedor_edit'),
    path('proveedores/eliminar/<int:id_proveedor>/', login_required(views.proveedor_delete), name='proveedor_delete'),

    # =======================
    # RUTAS DE EMPLEADOS
    # =======================
    path('empleados/', login_required(views.empleado_list), name='empleado_list'),
    path('empleados/crear/', login_required(views.empleado_create), name='empleado_create'),
    path('empleados/editar/<int:id_empleado>/', login_required(views.empleado_edit), name='empleado_edit'),
    path('empleados/eliminar/<int:id_empleado>/', login_required(views.empleado_delete), name='empleado_delete'),

    # =======================
    # RUTAS DE VENTAS
    # =======================
    path('ventas/', login_required(views.venta_list), name='venta_list'),
    path('ventas/crear/', login_required(views.venta_create), name='venta_create'),
    path('ventas/editar/<int:id_venta>/', login_required(views.venta_edit), name='venta_edit'),
    path('ventas/eliminar/<int:id_venta>/', login_required(views.venta_delete), name='venta_delete'),

    # =======================
    # RUTAS DE LOTES
    # =======================
    path('lotes/', login_required(views.lote_list), name='lote_list'),
    path('lotes/crear/', login_required(views.lote_create), name='lote_create'),
    path('lotes/editar/<int:id_lote>/', login_required(views.lote_edit), name='lote_edit'),
    path('lotes/eliminar/<int:id_lote>/', login_required(views.lote_delete), name='lote_delete'),

    # ==========================
    # RUTAS DE FACTURA COMPRA
    # ==========================
    path('facturas-compra/', login_required(views.facturacompra_list), name='facturacompra_list'),
    path('facturas-compra/crear/', login_required(views.facturacompra_create), name='facturacompra_create'),
    path('facturas-compra/editar/<int:id_factura_compra>/', login_required(views.facturacompra_edit), name='facturacompra_edit'),
    path('facturas-compra/eliminar/<int:id_factura_compra>/', login_required(views.facturacompra_delete), name='facturacompra_delete'),
    
    # ==========================
    # RUTAS LOTE_MEDICAMENTO
    # ==========================
    path('lote-medicamento/', login_required(views.lotemedicamento_list), name='lotemedicamento_list'),
    path('lote-medicamento/crear/', login_required(views.lotemedicamento_create), name='lotemedicamento_create'),
    path('lote-medicamento/editar/<int:id_lote_medicamento>/', login_required(views.lotemedicamento_edit), name='lotemedicamento_edit'),
    path('lote-medicamento/eliminar/<int:id_lote_medicamento>/', login_required(views.lotemedicamento_delete), name='lotemedicamento_delete'),
    
    # Rutas clientes
    path('clientes/', login_required(views.cliente_list), name='cliente_list'),
    path('clientes/nuevo/', login_required(views.cliente_create), name='cliente_create'),
    path('clientes/editar/<int:pk>/', login_required(views.cliente_edit), name='cliente_edit'),
    path('clientes/eliminar/<int:pk>/', login_required(views.cliente_delete), name='cliente_delete'),
    
    # CRUD DEVOLUCIONES
    path('devoluciones/', login_required(views.devolucioncliente_list), name='devolucion_list'),
    path('devoluciones/nueva/', login_required(views.devolucioncliente_create), name='devolucion_create'),
    path('devoluciones/editar/<int:pk>/', login_required(views.devolucioncliente_edit), name='devolucion_edit'),
    path('devoluciones/eliminar/<int:pk>/', login_required(views.devolucioncliente_delete), name='devolucion_delete'),
    
    # CRUD DE DEVOLUCIONES A PROVEEDOR
    path('devoluciones-proveedor/', login_required(views.devolucionproveedor_list), name='devolucionprov_list'),
    path('devoluciones-proveedor/nueva/', login_required(views.devolucionproveedor_create), name='devolucionprov_create'),
    path('devoluciones-proveedor/editar/<int:pk>/', login_required(views.devolucionproveedor_edit), name='devolucionprov_edit'),
    path('devoluciones-proveedor/eliminar/<int:pk>/', login_required(views.devolucionproveedor_delete), name='devolucionprov_delete'),
]