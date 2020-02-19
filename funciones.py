from flask import Flask, redirect, render_template, request
import os, shutil, stat, subprocess

def crear_carpeta(nombre, direccion_padre):
    direccion = os.path.join(direccion_padre, nombre)
    permisos = 0o770
    mensaje_exito = "Carpeta creada exitosamente"
    mensaje_error = "Este nombre pertenece a otra carpeta"
    try:
        os.mkdir(direccion, permisos)
        return render_template("respuesta.html", mensaje=mensaje_exito)
    except OSError:
        return render_template("respuesta.html", mensaje=mensaje_error)

def crear_archivo(nombre, direccion_padre):
    direccion = os.path.join(direccion_padre, nombre)
    permisos = 0o740
    mensaje_exito = "Archivo creado exitosamente"
    mensaje_error = "Este nombre pertenece a otro archivo"
    try:
        os.open(direccion, permisos)
        return render_template("respuesta.html", mensaje=mensaje_exito)
    except OSError:
        return render_template("respuesta.html", mensaje=mensaje_error)