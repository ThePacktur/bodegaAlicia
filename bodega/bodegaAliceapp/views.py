from django.shortcuts import render, redirect, get_object_or_404
from bodegaAliceapp.models import Productos, Distribuidor, Factura
from bodegaAliceapp.forms import FormProducto, FormDistribuidor, FormFactura

# Create your views here.

def index(request):
    return render(request, 'bodegaAliceapp/index.html')

def listadoProducto(request):
    productos = Productos.objects.all()
    data = {'productos': productos}
    return render(request, 'bodegaAliceapp/producto.html', data)

def listadoDistribuidor(request):
    distribuidores = Distribuidor.objects.all()
    data = {'distribuidores': distribuidores}
    return render(request, 'bodegaAliceapp/distribuidor.html', data)

def listadoFactura(request):
    facturas = Factura.objects.all()
    data = {'facturas': facturas}
    return render(request, 'bodegaAliceapp/factura.html', data)

def agregarProducto(request):
    form = FormProducto()
    if request.method == 'POST':
        form = FormProducto(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)  # Guarda pero no lo envía a la base aún
            producto.save()                    # Genera el QR al guardar
            return redirect('/productos')
    data = {'form': form}
    return render(request, 'bodegaAliceapp/agregarProducto.html', data)

def agregarDistribuidor(request):
    form = FormDistribuidor()
    if request.method == 'POST':
        form = FormDistribuidor(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/distribuidores')
    data = {'form': form}
    return render(request, 'bodegaAliceapp/agregarDistribuidor.html', data)

def agregarFactura(request):
    form = FormFactura()
    if request.method == 'POST':
        form = FormFactura(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect('/facturas')
    data = {'form': form}
    return render(request, 'bodegaAliceapp/agregarFactura.html', data)

def eliminarProducto(request, pk):
    producto = get_object_or_404(Productos, pk=pk)
    producto.delete()
    return redirect('/productos')

def eliminarDistribuidor(request, pk):
    distribuidor = get_object_or_404(Distribuidor, pk=pk)
    distribuidor.delete()
    return redirect('/distribuidores')

def eliminarFactura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    factura.delete()
    return redirect('/facturas')

def actualizarProducto(request, pk):
    producto = get_object_or_404(Productos, pk=pk)
    form = FormProducto(instance=producto)
    if request.method == 'POST':
        form = FormProducto(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)  # Guarda pero no lo envía a la base aún
            producto.save()                    # Actualiza el QR al guardar
            return redirect('/productos')
    data = {'form': form}
    return render(request, 'bodegaAliceapp/agregarProducto.html', data)

def actualizarDistribuidores(request, pk):
    distribuidor = get_object_or_404(Distribuidor, pk=pk)
    form = FormDistribuidor(instance=distribuidor)
    if request.method == 'POST':
        form = FormDistribuidor(request.POST, instance=distribuidor)
        if form.is_valid():
            form.save()
        return redirect('/distribuidores')
    data = {'form': form}
    return render(request, 'bodegaAliceapp/agregarDistribuidor.html', data)

def actualizarFactura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    form = FormFactura(instance=factura)
    if request.method == 'POST':
        form = FormFactura(request.POST, instance=factura)
        if form.is_valid():
            form.save()
        return redirect('/facturas')
    data = {'form': form}
    return render(request, 'bodegaAliceapp/agregarFactura.html', data)
