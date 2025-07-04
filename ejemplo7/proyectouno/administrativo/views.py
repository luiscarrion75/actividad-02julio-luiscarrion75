from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.db import models
from django.db.models import Sum

# importar las clases de models.py
from administrativo.models import Matricula, Estudiante, Modulo
from administrativo.forms import *

# vista que permita presesentar las matriculas
# el nombre de la vista es index.

def index(request):
    """
    """
    matriculas = Matricula.objects.all()

    titulo = "Listado de matriculas"
    informacion_template = {'matriculas': matriculas,
    'numero_matriculas': len(matriculas), 'mititulo': titulo}
    return render(request, 'index.html', informacion_template)


def detalle_matricula(request, id):
    """

    """

    matricula = Matricula.objects.get(pk=id)
    informacion_template = {'matricula': matricula}
    return render(request, 'detalle_matricula.html', informacion_template)


def crear_matricula(request):
    """
    """
    if request.method=='POST':
        formulario = MatriculaForm(request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save() # se guarda en la base de datos
            return redirect(index)
    else:
        formulario = MatriculaForm()
    diccionario = {'formulario': formulario}

    return render(request, 'crear_matricula.html', diccionario)

def editar_matricula(request, id):
    """
    """
    matricula = Matricula.objects.get(pk=id)
    print("----------matricula")
    print(matricula)
    print("----------matricula")
    if request.method=='POST':
        formulario = MatriculaEditForm(request.POST, instance=matricula)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = MatriculaEditForm(instance=matricula)
    diccionario = {'formulario': formulario}

    return render(request, 'crear_matricula.html', diccionario)

def detalle_estudiante(request, id):
    """

    """

    estudiante = Estudiante.objects.get(pk=id)
    informacion_template = {'e': estudiante}
    return render(request, 'detalle_estudiante.html', informacion_template)

# ver los módulos
#    nombre del módulp
#    valor de todas las matriculas del módulo    
def ver_modulos(request):
    """
    Vista que muestra el listado de módulos y el valor de todas las matrículas asociadas.
    """
    modulos = Modulo.objects.all()  # Traemos todos los módulos
    modulos_info = []

    for modulo in modulos:
        # Cambia matricula_set por lasmatriculas, que es el related_name en la relación de Matricula
        total_valor = modulo.lasmatriculas.aggregate(total=Sum('costo'))['total']  # Usamos 'costo' ya que es el campo que guarda el valor de la matrícula
        
        modulos_info.append({
            'modulo': modulo,
            'total_valor': total_valor if total_valor else 0
        })

    informacion_template = {'modulos_info': modulos_info, 'mititulo': "Listado de Módulos"}
    return render(request, 'ver_modulos.html', informacion_template)

# ver los estudiantes >> de los estudiantes debo visualizar:
#    nombre 
#    apellido
#    cedula
#    edad
#    tipo_estudiante 
#    costo de matriculas

def ver_estudiantes(request):
    """
    Vista que muestra los estudiantes con su nombre, apellido, cédula, edad, tipo de estudiante y el costo de matrícula.
    """
    estudiantes = Estudiante.objects.all()
    estudiantes_info = []

    for estudiante in estudiantes:
        matriculas = estudiante.lasmatriculas.all()  # Usamos 'lasmatriculas.all()' para obtener las matrículas
        total_costo = sum(matricula.costo for matricula in matriculas)  # Sumamos los valores de las matrículas

        # Si también deseas sumar el valor de los módulos
        total_valor_modulos = sum(matricula.modulo.valor for matricula in matriculas if matricula.modulo.valor)  # Suma el valor de los módulos asociados
        
        estudiantes_info.append({
            'estudiante': estudiante,
            'total_costo': total_costo,
            'total_valor_modulos': total_valor_modulos
        })

    informacion_template = {'estudiantes_info': estudiantes_info, 'mititulo': "Listado de Estudiantes"}
    return render(request, 'ver_estudiantes.html', informacion_template)

# crear módulos

def crear_modulo(request):
    """
    Vista para crear un nuevo módulo.
    """
    if request.method == 'POST':
        formulario = ModuloForm(request.POST)
        if formulario.is_valid():
            formulario.save()  # Guardamos el nuevo módulo
            return redirect('ver_modulos')  # Redirigir al listado de módulos
    else:
        formulario = ModuloForm()

    diccionario = {'formulario': formulario}
    return render(request, 'crear_modulo.html', diccionario)

# crear estudiantes

def crear_estudiante(request):
    """
    Vista para crear un nuevo estudiante.
    """
    if request.method == 'POST':
        formulario = EstudianteForm(request.POST)
        if formulario.is_valid():
            formulario.save()  # Guardamos el nuevo estudiante
            return redirect('ver_estudiantes')  # Redirigir al listado de estudiantes
    else:
        formulario = EstudianteForm()

    diccionario = {'formulario': formulario}
    return render(request, 'crear_estudiante.html', diccionario)
