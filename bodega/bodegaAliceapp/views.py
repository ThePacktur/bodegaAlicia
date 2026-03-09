from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from bodegaAliceapp.forms import FormDistribuidor, FormFactura, FormProducto
from bodegaAliceapp.models import Distribuidor, Factura, Productos


def index(request):
    return render(request, 'bodegaAliceapp/index.html')


def listadoProducto(request):
    productos = Productos.objects.prefetch_related('distribuidores', 'facturas').order_by('idProducto')
    return render(request, 'bodegaAliceapp/producto.html', {'productos': productos})


def listadoDistribuidor(request):
    distribuidores = Distribuidor.objects.order_by('idDistribuidor')
    return render(request, 'bodegaAliceapp/distribuidor.html', {'distribuidores': distribuidores})


def listadoFactura(request):
    facturas = Factura.objects.select_related('distribuidor').order_by('idFactura')
    return render(request, 'bodegaAliceapp/factura.html', {'facturas': facturas})


def agregarProducto(request):
    form = FormProducto(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('productos'))
    return render(request, 'bodegaAliceapp/agregarProducto.html', {'form': form})


def agregarDistribuidor(request):
    form = FormDistribuidor(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('distribuidores'))
    return render(request, 'bodegaAliceapp/agregarDistribuidor.html', {'form': form})


def agregarFactura(request):
    form = FormFactura(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('facturas'))
    return render(request, 'bodegaAliceapp/agregarFactura.html', {'form': form})


def eliminarProducto(request, pk):
    producto = get_object_or_404(Productos, pk=pk)
    producto.delete()
    return redirect(reverse('productos'))


def eliminarDistribuidor(request, pk):
    distribuidor = get_object_or_404(Distribuidor, pk=pk)
    distribuidor.delete()
    return redirect(reverse('distribuidores'))


def eliminarFactura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    factura.delete()
    return redirect(reverse('facturas'))


def actualizarProducto(request, pk):
    producto = get_object_or_404(Productos, pk=pk)
    form = FormProducto(request.POST or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('productos'))
    return render(request, 'bodegaAliceapp/agregarProducto.html', {'form': form})


def actualizarDistribuidores(request, pk):
    distribuidor = get_object_or_404(Distribuidor, pk=pk)
    form = FormDistribuidor(request.POST or None, instance=distribuidor)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('distribuidores'))
    return render(request, 'bodegaAliceapp/agregarDistribuidor.html', {'form': form})


def actualizarFactura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    form = FormFactura(request.POST or None, instance=factura)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('facturas'))
    return render(request, 'bodegaAliceapp/agregarFactura.html', {'form': form})
