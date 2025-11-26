from django.urls import path
from . import views

urlpatterns = [
    # Home temporal
    path('', views.home, name='home'),

    # =======================
    # RUTAS DE MEDICAMENTOS
    # =======================
    path('medicamentos/', views.medicamento_list, name='medicamento_list'),
    path('medicamentos/crear/', views.medicamento_create, name='medicamento_create'),
    path('medicamentos/editar/<int:id_medicamento>/', views.medicamento_edit, name='medicamento_edit'),
    path('medicamentos/eliminar/<int:id_medicamento>/', views.medicamento_delete, name='medicamento_delete'),

    # =======================
    # RUTAS DE PROVEEDORES
    # =======================
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/crear/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/editar/<int:id_proveedor>/', views.proveedor_edit, name='proveedor_edit'),
    path('proveedores/eliminar/<int:id_proveedor>/', views.proveedor_delete, name='proveedor_delete'),

    # =======================
    # RUTAS DE EMPLEADOS
    # =======================
    path('empleados/', views.empleado_list, name='empleado_list'),
    path('empleados/crear/', views.empleado_create, name='empleado_create'),
    path('empleados/editar/<int:id_empleado>/', views.empleado_edit, name='empleado_edit'),
    path('empleados/eliminar/<int:id_empleado>/', views.empleado_delete, name='empleado_delete'),

    # =======================
    # RUTAS DE VENTAS
    # =======================
    path('ventas/', views.venta_list, name='venta_list'),
    path('ventas/crear/', views.venta_create, name='venta_create'),
    path('ventas/editar/<int:id_venta>/', views.venta_edit, name='venta_edit'),
    path('ventas/eliminar/<int:id_venta>/', views.venta_delete, name='venta_delete'),

    # =======================
    # RUTAS DE LOTES
    # =======================
    path('lotes/', views.lote_list, name='lote_list'),
    path('lotes/crear/', views.lote_create, name='lote_create'),
    path('lotes/editar/<int:id_lote>/', views.lote_edit, name='lote_edit'),
    path('lotes/eliminar/<int:id_lote>/', views.lote_delete, name='lote_delete'),

    # ==========================
    # RUTAS DE FACTURA COMPRA
    # ==========================

    path('facturas-compra/', views.facturacompra_list, name='facturacompra_list'),
    path('facturas-compra/crear/', views.facturacompra_create, name='facturacompra_create'),
    path('facturas-compra/editar/<int:id_factura_compra>/', views.facturacompra_edit, name='facturacompra_edit'),
    path('facturas-compra/eliminar/<int:id_factura_compra>/', views.facturacompra_delete, name='facturacompra_delete'),
    
    # ==========================
    # RUTAS LOTE_MEDICAMENTO
    # ==========================

    path('lote-medicamento/', views.lotemedicamento_list, name='lotemedicamento_list'),
    path('lote-medicamento/crear/', views.lotemedicamento_create, name='lotemedicamento_create'),
    path('lote-medicamento/editar/<int:id_lote_medicamento>/', views.lotemedicamento_edit, name='lotemedicamento_edit'),
    path('lote-medicamento/eliminar/<int:id_lote_medicamento>/', views.lotemedicamento_delete, name='lotemedicamento_delete'),
    
    #Rutas clientes
    
    path('clientes/', views.cliente_list, name='cliente_list'),                # Lista clientes
    path('clientes/nuevo/', views.cliente_create, name='cliente_create'),      # Crear cliente
    path('clientes/editar/<int:pk>/', views.cliente_edit, name='cliente_edit'),# Editar cliente
    path('clientes/eliminar/<int:pk>/', views.cliente_delete, name='cliente_delete'), # Eliminar client
    # CRUD DEVOLUCIONES
    path('devoluciones/', views.devolucioncliente_list, name='devolucion_list'),
    path('devoluciones/nueva/', views.devolucioncliente_create, name='devolucion_create'),
    path('devoluciones/editar/<int:pk>/', views.devolucioncliente_edit, name='devolucion_edit'),
    path('devoluciones/eliminar/<int:pk>/', views.devolucioncliente_delete, name='devolucion_delete'),
    # CRUD DE DEVOLUCIONES A PROVEEDOR
    path('devoluciones-proveedor/', views.devolucionproveedor_list, name='devolucionprov_list'),
    path('devoluciones-proveedor/nueva/', views.devolucionproveedor_create, name='devolucionprov_create'),
    path('devoluciones-proveedor/editar/<int:pk>/', views.devolucionproveedor_edit, name='devolucionprov_edit'),
    path('devoluciones-proveedor/eliminar/<int:pk>/', views.devolucionproveedor_delete, name='devolucionprov_delete'),


]
