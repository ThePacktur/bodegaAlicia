from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from bodegaAliceapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('productos/', views.listadoProducto, name='productos'),
    path('agregarProducto/', views.agregarProducto, name='agregar_producto'),
    path('eliminarProducto/<pk>', views.eliminarProducto, name='eliminar_producto'),
    path('actualizarProducto/<pk>', views.actualizarProducto, name='actualizar_producto'),
    path('distribuidores/', views.listadoDistribuidor, name='distribuidores'),
    path('agregarDistribuidor/', views.agregarDistribuidor, name='agregar_distribuidor'),
    path('eliminarDistribuidor/<pk>', views.eliminarDistribuidor, name='eliminar_distribuidor'),
    path('actualizarDistribuidor/<pk>', views.actualizarDistribuidores, name='actualizar_distribuidor'),
    path('facturas/', views.listadoFactura, name='facturas'),
    path('agregarFactura/', views.agregarFactura, name='agregar_factura'),
    path('eliminarFactura/<pk>', views.eliminarFactura, name='eliminar_factura'),
    path('actualizarFactura/<pk>', views.actualizarFactura, name='actualizar_factura'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
