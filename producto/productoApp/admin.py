from django.contrib import admin
from productoApp.models import Productos, Distribuidor, Factura
from django.core.exceptions import ValidationError

class ProductosAdmin(admin.ModelAdmin):
    list_display = ['nombreProducto', 'descripcion', 'categoria', 'denominacionOrigen', 'cantidadProducto']
    search_fields = ['nombreProducto', 'categoria']
    list_filter = ['categoria']

class DistribuidorAdmin(admin.ModelAdmin):
    list_display = ['telefono', 'email', 'ciudad', 'fechaDespacho', 'fechaRecepcion']
    search_fields = ['ciudad', 'email']
    list_filter = ['ciudad', 'fechaDespacho']

    def save_model(self, request, obj, form, change):
        # Validación personalizada al guardar un distribuidor
        if obj.fechaDespacho > obj.fechaRecepcion:
            raise ValidationError("La fecha de recepción debe ser igual o posterior a la fecha de despacho.")
        super().save_model(request, obj, form, change)

class FacturaAdmin(admin.ModelAdmin):
    list_display = ['fechaFacturacion', 'precioUnitario', 'iva', 'descuentoTotal', 'totalApagar']
    search_fields = ['fechaFacturacion']
    list_filter = ['fechaFacturacion', 'iva']

    def save_model(self, request, obj, form, change):
        # Validación personalizada al guardar una factura
        if obj.totalApagar < 0:
            raise ValidationError("El total a pagar no puede ser negativo.")
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Productos, ProductosAdmin)
admin.site.register(Distribuidor, DistribuidorAdmin)
admin.site.register(Factura, FacturaAdmin)