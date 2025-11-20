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
]
