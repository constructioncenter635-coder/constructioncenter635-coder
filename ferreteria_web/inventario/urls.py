from django.urls import path
from . import views
from . import ventas_views  # vistas de ventas

urlpatterns = [
    # -----------------------------
    # Página principal
    # -----------------------------
    path('', views.lista_productos, name='inicio'),

    # -----------------------------
    # Inventario    
    # -----------------------------
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('importar/', views.importar_excel, name='importar_excel'),

    # -----------------------------
    # Ventas
    # -----------------------------
    path('ventas/', ventas_views.listar_ventas, name='listar_ventas'),
    path('ventas/nueva/', ventas_views.registrar_venta, name='ventas_nueva'),
    path('ventas/smartclick/<int:sale_id>/', ventas_views.smartclick_redirect, name='smartclick_redirect'),
    path('ventas/nota/<int:sale_id>/', ventas_views.nota_venta, name='nota_venta'),

    # -----------------------------
    # Caja
    # -----------------------------
    path("historial-caja/", ventas_views.historial_caja, name="historial_cajas"),
    path("caja/abrir/", ventas_views.abrir_caja, name="abrir_caja"),
    path("caja/cerrar/<int:caja_id>/", ventas_views.cerrar_caja, name="cerrar_caja"),
    path("ventas/cerrar/<str:periodo>/<str:valor>/", ventas_views.cerrar_caja_periodo, name="cerrar_caja_periodo"),

    # -----------------------------
    # API
    # -----------------------------
    path('api/producto/<int:pk>/', views.producto_api, name='producto_api'),

    # -----------------------------
    # Autenticación
    # -----------------------------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
