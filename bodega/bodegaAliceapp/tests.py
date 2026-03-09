from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from bodegaAliceapp.forms import FormDistribuidor
from bodegaAliceapp.models import Distribuidor, Factura, Productos


class FormDistribuidorTest(TestCase):
    def test_email_repetido_es_invalido_en_nuevo_registro(self):
        Distribuidor.objects.create(
            telefono='3001234567',
            email='demo@bodega.com',
            ciudad='Bogota',
            fechaDespacho=date(2024, 1, 1),
            fechaRecepcion=date(2024, 1, 2),
        )

        form = FormDistribuidor(
            data={
                'telefono': '3111234567',
                'email': 'demo@bodega.com',
                'ciudad': 'Cali',
                'fechaDespacho': '2024-02-01',
                'fechaRecepcion': '2024-02-02',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_email_igual_en_actualizacion_del_mismo_distribuidor_es_valido(self):
        distribuidor = Distribuidor.objects.create(
            telefono='3001234567',
            email='demo@bodega.com',
            ciudad='Bogota',
            fechaDespacho=date(2024, 1, 1),
            fechaRecepcion=date(2024, 1, 2),
        )

        form = FormDistribuidor(
            instance=distribuidor,
            data={
                'telefono': '3001234567',
                'email': 'demo@bodega.com',
                'ciudad': 'Medellin',
                'fechaDespacho': '2024-01-01',
                'fechaRecepcion': '2024-01-02',
            },
        )
        self.assertTrue(form.is_valid())


class FacturaModelTest(TestCase):
    def test_total_a_pagar_calculado_con_decimal(self):
        factura = Factura(
            fechaFacturacion=date(2024, 1, 1),
            precioUnitario=Decimal('100.00'),
            iva=Decimal('19.00'),
            descuentoTotal=Decimal('10.00'),
        )
        self.assertEqual(factura.totalApagar, Decimal('109.00'))


class ProductosViewTest(TestCase):
    def test_post_invalido_no_redirige_y_retorna_formulario(self):
        response = self.client.post(
            reverse('agregar_producto'),
            {
                'nombreProducto': '',
                'descripcion': 'Demo',
                'categoria': 'Bebidas',
                'denominacionOrigen': 'Colombia',
                'cantidadProducto': 1,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_post_valido_crea_producto_y_redirige(self):
        response = self.client.post(
            reverse('agregar_producto'),
            {
                'nombreProducto': 'Cafe',
                'descripcion': 'Cafe premium',
                'categoria': 'Bebidas',
                'denominacionOrigen': 'Colombia',
                'cantidadProducto': 10,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Productos.objects.count(), 1)
