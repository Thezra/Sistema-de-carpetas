from flask import Flask, redirect, render_template, request
import os, shutil, stat, subprocess

def crear_carpeta(nombre, direccion_padre):
    direccion = os.path.join(direccion_padre, nombre)
    permisos = 0o770
    mensaje = "Carpeta creada exitosamente"
    os.mkdir(direccion, permisos)
    return render_template("success.html", mensaje=mensaje)

def crear_archivo(nombre, direccion_padre):
    direccion = os.path.join(direccion_padre, nombre)
    permisos = 0o740
    mensaje = "Archivo creado exitosamente donde se le dió la gana"
    os.open(direccion, permisos)
    return render_template("success.html", mensaje=mensaje)