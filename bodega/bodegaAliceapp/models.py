from decimal import Decimal
from io import BytesIO

import qrcode
import qrcode.constants
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _


def validacion_positivo(value):
    """Valida que el valor recibido no sea negativo."""
    if value < 0:
        raise ValidationError(
            _('%(value)s debe ser un número positivo.'),
            params={'value': value},
        )


class Distribuidor(models.Model):
    idDistribuidor = models.AutoField(primary_key=True)
    telefono = models.CharField(max_length=50)
    email = models.EmailField()
    ciudad = models.CharField(max_length=15)
    fechaDespacho = models.DateField()
    fechaRecepcion = models.DateField()

    def clean(self):
        if self.fechaDespacho > self.fechaRecepcion:
            raise ValidationError(
                {'fechaRecepcion': _('La fecha de recepción debe ser igual o posterior a la fecha de despacho.')}
            )

        if not self.telefono.isdigit():
            raise ValidationError({'telefono': _('El número de teléfono debe contener solo dígitos.')})
        if len(self.telefono) < 10:
            raise ValidationError({'telefono': _('El número de teléfono debe tener al menos 10 dígitos.')})

    def __str__(self):
        return f'Distribuidor: {self.idDistribuidor} - {self.ciudad}'


class Factura(models.Model):
    idFactura = models.AutoField(primary_key=True)
    distribuidor = models.ForeignKey(
        Distribuidor,
        on_delete=models.CASCADE,
        related_name='facturas',
        null=True,
        blank=True,
    )
    fechaFacturacion = models.DateField()
    precioUnitario = models.DecimalField(max_digits=15, decimal_places=2, validators=[validacion_positivo])
    iva = models.DecimalField(max_digits=5, decimal_places=2, validators=[validacion_positivo])
    descuentoTotal = models.DecimalField(max_digits=15, decimal_places=2, validators=[validacion_positivo])

    @property
    def totalApagar(self):
        """Calcula automáticamente el total a pagar con precisión Decimal."""
        total = (self.precioUnitario * (Decimal('1') + (self.iva / Decimal('100')))) - self.descuentoTotal
        return total.quantize(Decimal('0.01'))

    def clean(self):
        if self.totalApagar < 0:
            raise ValidationError(_('El total a pagar no puede ser negativo.'))

    def __str__(self):
        return f'Factura: {self.idFactura} - Precio Total: {self.totalApagar}'


class Productos(models.Model):
    idProducto = models.AutoField(primary_key=True)
    distribuidores = models.ManyToManyField(Distribuidor, related_name='productos', blank=True)
    facturas = models.ManyToManyField(Factura, related_name='productos', blank=True)
    nombreProducto = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=50)
    categoria = models.CharField(max_length=50)
    denominacionOrigen = models.CharField(max_length=50)
    cantidadProducto = models.IntegerField(validators=[validacion_positivo])
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def generate_qr_code(self):
        """Genera el código QR con la metadata principal del producto."""
        factura = self.facturas.select_related('distribuidor').first()
        distribuidor = factura.distribuidor if factura else None

        qr_data = {
            'Producto': self.nombreProducto,
            'Descripcion': self.descripcion,
            'Categoria': self.categoria,
            'Denominacion de origen': self.denominacionOrigen or 'N/A',
            'Cantidad': self.cantidadProducto,
            'Factura': factura.pk if factura else 'Sin Factura',
            'Distribuidor': distribuidor.pk if distribuidor else 'Sin Distribuidor',
        }

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        image = qr.make_image(fill_color='black', back_color='white')
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)

        self.qr_code.save(f'qr_{self.pk}.png', File(buffer), save=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_qr_code()
        super().save(update_fields=['qr_code'])

    def __str__(self):
        return f'Producto: {self.idProducto} - {self.nombreProducto}'
