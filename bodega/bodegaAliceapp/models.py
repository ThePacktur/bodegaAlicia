import qrcode
from django.db import models
from io import BytesIO
from django.core.files import File
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

import qrcode.constants
# Función de validación que verifica si un valor es positivo
def validacion_positivo(value):
    if value < 0:
        raise ValidationError(_('%(value)s debe ser un número positivo.'), params={'value': value},)

class Distribuidor(models.Model):
    idDistribuidor = models.AutoField(primary_key=True)
    telefono = models.CharField(max_length=50)
    email = models.EmailField()
    ciudad = models.CharField(max_length=15)
    fechaDespacho = models.DateField()
    fechaRecepcion = models.DateField()
    
    def clean(self):
        if self.fechaDespacho > self.fechaRecepcion:
            raise ValidationError({
                'fechaRecepcion': _('La fecha de recepción debe ser igual o posterior a la fecha de despacho.')
            })
        
        if not self.telefono.isdigit():
            raise ValidationError({'telefono': _('El número de teléfono debe contener solo dígitos.')})
        if len(self.telefono) < 10:
            raise ValidationError({'telefono': _('El número de teléfono debe tener al menos 10 dígitos.')})
    def __str__(self):
        return f'Distribuidor: {self.idDistribuidor} - {self.ciudad}'

class Factura(models.Model):
    idFactura = models.AutoField(primary_key=True)
    distribuidor = models.ForeignKey(Distribuidor, on_delete=models.CASCADE, related_name="facturas", null=True, blank=True)
    fechaFacturacion = models.DateField()
    precioUnitario = models.DecimalField(max_digits=15, decimal_places=2, validators=[validacion_positivo])
    iva = models.DecimalField(max_digits=5, decimal_places=2, validators=[validacion_positivo])
    descuentoTotal = models.DecimalField(max_digits=15, decimal_places=2, validators=[validacion_positivo])
    
    @property
    def totalApagar(self):
        """Calcula automáticamente el total a pagar."""
        return round((self.precioUnitario * (1 + self.iva / Decimal('100'))) - self.descuentoTotal, 2)

    def clean(self):
        if self.totalApagar < 0:  # Asegúrate de que el total no sea negativo
            raise ValidationError(_('El total a pagar no puede ser negativo.'))

    def __str__(self):
        return f'Factura: {self.idFactura} - Precio Total: {self.totalApagar}'

class Productos(models.Model):
    idProducto = models.AutoField(primary_key=True)
    distribuidores = models.ManyToManyField(Distribuidor, related_name="productos", null=True, blank=True)
    facturas = models.ManyToManyField(Factura, related_name="productos", null=True, blank=True)
    nombreProducto = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=50)
    categoria = models.CharField(max_length=50)
    denominacionOrigen = models.CharField(max_length=50)
    cantidadProducto = models.IntegerField(validators=[validacion_positivo])
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def generate_qr_code(self):
        # Información a incluir en el QR
        factura = self.facturas.first()  # Corregido: Usar 'facturas.first()' en lugar de 'facturas_set.first()'
        distribuidor = factura.distribuidor if factura else None  # Acceder correctamente al distribuidor

        qr_data = {
            'Producto': self.nombreProducto,
            'Descripcion': self.descripcion,
            'Categoria': self.categoria,
            'Denominacion de origen': self.denominacionOrigen or 'N/A',
            'Cantidad': self.cantidadProducto,
            'Factura': factura.id if factura else 'Sin Factura',
            'Distribuidor': distribuidor.id if distribuidor else 'Sin Distribuidor'
        }

        # Crear el QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Convertir el QR en imagen
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)

        # Guardar el QR en el campo del modelo
        self.qr_code.save(f'qr_{self.pk}.png', File(buffer), save=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda el producto primero
        self.generate_qr_code()  # Genera y guarda el QR
        super().save(*args, **kwargs)  # Guarda nuevamente el QR actualizado

    def __str__(self):
        return f'Producto: {self.idProducto} - {self.nombreProducto}'