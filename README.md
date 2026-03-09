# Bodega Alicia

Aplicación web desarrollada con **Django** para administrar una bodega:
- Gestión de **productos**.
- Gestión de **distribuidores**.
- Gestión de **facturas**.
- Generación automática de **códigos QR** por producto con metadata básica.

## Características principales

- CRUD completo para Productos, Distribuidores y Facturas.
- Validaciones de negocio en formularios y modelos:
  - Teléfono solo numérico y mínimo de 10 dígitos.
  - Fecha de recepción no puede ser menor a la fecha de despacho.
  - Totales monetarios y descuentos no negativos.
- Cálculo automático del total de factura (`totalApagar`).
- Código QR generado y persistido al guardar productos.
- Configuración más robusta por variables de entorno (modo SQLite para desarrollo y MySQL opcional).

## Estructura del proyecto

```text
bodega/
├── bodega/                  # Configuración global de Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── bodegaAliceapp/          # App principal
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── tests.py
│   └── ...
├── static/                  # Archivos estáticos
├── templates/               # Plantillas HTML
└── manage.py
```

## Requisitos

- Python 3.10+
- pip
- (Opcional) MySQL, si deseas usar base de datos MySQL en vez de SQLite.

Dependencias principales:
- Django
- qrcode
- pymysql

## Instalación rápida

1. Clona el repositorio.
2. Crea y activa entorno virtual.
3. Instala dependencias.
4. Ejecuta migraciones.
5. Inicia servidor.

```bash
cd bodega
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

> Si no existe `requirements.txt`, instala manualmente: `django`, `qrcode`, `pymysql`, `Pillow`.

## Configuración por variables de entorno

`bodega/settings.py` permite configuración flexible:

- `DJANGO_SECRET_KEY`: clave secreta.
- `DJANGO_DEBUG`: `True|False`.
- `DJANGO_ALLOWED_HOSTS`: hosts separados por coma.
- `USE_SQLITE`: `1` (default) usa SQLite; `0` usa MySQL.
- `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`.

### Ejemplo (MySQL)

```bash
export USE_SQLITE=0
export MYSQL_DATABASE=alicebd
export MYSQL_USER=root
export MYSQL_PASSWORD=tu_password
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
```

## Ejecución de pruebas

Desde `bodega/`:

```bash
python manage.py test
```

## Endpoints principales

- `/` Inicio
- `/productos/`
- `/agregarProducto/`
- `/distribuidores/`
- `/agregarDistribuidor/`
- `/facturas/`
- `/agregarFactura/`

## Mejoras aplicadas en esta actualización

- Refactor de vistas para manejar correctamente formularios inválidos sin redirecciones prematuras.
- Uso de `reverse` y rutas nombradas para mantener URLs consistentes.
- Optimización de consultas (`select_related`, `prefetch_related`, `order_by`).
- Corrección de validación de email de distribuidores en edición.
- Mejora de precisión monetaria con `Decimal.quantize`.
- Robustez del QR (IDs correctos de factura/distribuidor y persistencia explícita del campo).
- Documentación técnica inicial del proyecto.

## Recomendaciones siguientes

- Agregar autenticación y autorización por roles.
- Separar settings por entorno (`dev`, `test`, `prod`).
- Centralizar estilo de plantillas con un `base.html`.
- Integrar CI para pruebas automáticas.
