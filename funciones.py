from flask import Flask, redirect, render_template, request
import os, shutil, stat, subprocess

def crear_carpeta(nombre, direccion_padre):
    direccion = os.path.join(direccion_padre, nombre)
    permisos = 0o770
    mensaje_exito = "Carpeta creada exitosamente"
    mensaje_error = "Este nombre pertenece a otro archivo o carpeta"
    try:
        os.mkdir(direccion, permisos)
        return render_template("exito.html", mensaje=mensaje_exito)
    except OSError:
        return render_template("error.html", mensaje=mensaje_error)

def crear_archivo(nombre, direccion_padre):
    direccion = os.path.join(direccion_padre, nombre)
    permisos = 0o740
    mensaje_exito = "Archivo creado exitosamente"
    mensaje_error = "Este nombre pertenece a otro archivo o carpeta"
    try:
        os.open(direccion, permisos)
        return render_template("exito.html", mensaje=mensaje_exito)
    except OSError:
        return render_template("error.html", mensaje=mensaje_error)

def mostrar_permisos(nombre, Ruta):
	mensaje_error = "Ha habido un error al buscar la ruta"
	try:
		resultado=subprocess.getoutput(["ls -l "+Ruta+nombre])
		return render_template("ventana.html", mensaje=resultado)
	except OSError:
		return render_template("error.html", mensaje=mensaje_error)
    #comando = "ls -l | grep "+str(nombre)
    #salida = os.system(comando)
    #return str(resultado)
'''def mostrar_permisos(nombre, Ruta):
	mensaje_error = "Ha habido un error al buscar la ruta"
	try:
		resultado=subprocess.Popen(["ls", "-p", Ruta+nombre], stdout=subprocess.PIPE,)
		return render_template("ventana.html", mensaje=resultado)
	except OSError:
		return render_template("error.html", mensaje=mensaje_error)'''
