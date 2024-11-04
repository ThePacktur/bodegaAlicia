from django.shortcuts import render, redirect
from productoApp.models import Productos, Distribuidor, Factura
from productoApp.forms import FormProducto, FormDistribuidor, FormFactura

# Create your views here.

def index(request):
    return render(request, 'productoApp/index.html')

def listadoProducto(request):
    productos = Productos.objects.all()
    data = {'productos': productos}
    return render(request, 'productoApp/producto.html', data)

def listadoDistribuidor(request):
    distribuidores = Distribuidor.objects.all()
    data = {'distribuidores': distribuidores}
    return render(request, 'productoApp/distribuidor.html', data)


def listadoFactura(request):
    facturas = Factura.objects.all()
    data = {'facturas' : facturas}
    return render(request, 'productoApp/factura.html', data)

def agregarProducto(request):
    form = FormProducto
    if request.method == 'POST':
        form = FormProducto(request.POST)
        if form.is_valid():
            form.save()
        return listadoProducto(request)
    data = {'form': form}
    return render(request,'productoApp/agregarProducto.html', data)

def agregarDistribuidor(request):
    form = FormDistribuidor()
    if request.method == 'POST':
        form = FormDistribuidor(request.POST)
        if form.is_valid():
            form.save()
        return listadoDistribuidor(request)
    data = {'form': form}
    return render(request, 'productoApp/agregarDistribuidor.html', data)

def agregarFactura(request):
    form = FormFactura
    if request.method == 'POST':
        form = FormFactura(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return listadoFactura(request)
    data = {'form': form}
    return render(request, 'productoApp/agregarFactura.html', data)


def eliminarProducto(request, pk):
    producto = Productos.objects.get(pk = pk)
    producto.delete()
    return redirect('/productos')

def eliminarDistribuidor(request, pk):
    distribuidor = Distribuidor.objects.get(pk=pk)
    distribuidor.delete()
    return redirect('/distribuidores')

def eliminarFactura(request, pk):
    factura = Factura.objects.get(pk = pk)
    factura.delete()
    return redirect('/facturas')


def actualizarProducto(request, pk):
    producto = Productos.objects.get(pk = pk)
    form = FormProducto(instance=producto)
    if request.method == 'POST':
        form = FormProducto(request.POST, instance=producto)
        if form.is_valid(): 
            form.save()
        return listadoProducto(request)
    data = {'form': form}
    return render(request, 'productoApp/agregarProducto.html', data)

def actualizarDistribuidores(request, pk):
    distribuidor = Distribuidor.objects.get(pk = pk)
    form = FormDistribuidor(instance=distribuidor)
    if request.method == 'POST':
        form = FormDistribuidor(request.POST, instance=distribuidor)
        if form.is_valid():
            form.save()
        return listadoDistribuidor(request)
    data = {'form': form}
    return render(request, 'productoApp/agregarDistribuidor.html', data)

def actualizarFactura(request, pk):
    factura = Factura.objects.get(pk=pk)
    form = FormFactura(instance=factura)
    if request.method == "POST":
        form = FormFactura(request.POST, instance=factura)
        if form.is_valid():
            form.save()
        return listadoFactura(request)
    data = {'form': form}
    return render(request, 'productoApp/agregarFactura.html',data)