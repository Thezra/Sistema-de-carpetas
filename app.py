from flask import Flask, redirect
import os, shutil

app = Flask(__name__)

@app.route('/')
def inicio():
    return redirect('/Home')

#muestra la carpeta home automaticamente al inicar
@app.route('/Home')
def mostrar_home():
    lista_archivos = mostrar_contenido_carpeta('~')
    return str(lista_archivos)
    
    

#Muestra el contenido de la carpeta
def mostrar_contenido_carpeta(carpeta):
    home = os.path.expanduser(carpeta)
    lista_directorios = os.listdir(home)
    return lista_directorios
    
#Crea una nueva carpeta
def crear_carpeta(nombre, direccion_padre):
    direccion = os.path.join(direccion_padre, nombre)
    permisos = 0o770
    mensaje = ""
    if os.path.exists(direccion):
        mensaje = "La carpeta no puede crearse, ya existe."
    else:
        os.mkdir(direccion, permisos)
        if os.path.exists(direccion):
            mensaje =  "Carpeta {} creada correctamente.".format(nombre)
    return mensaje

#Crea un nuevo archivo
def crear_archivo(nombre,direccion_padre):
    direccion = os.path.join(direccion_padre, nombre)
    permisos = 0o740
    mensaje = ""
    if os.path.exists(direccion):
        mensaje = "El archivo no puede crearse, ya existe."
    else:
        os.open(nombre, permisos)
        if os.path.exists(direccion):
            mensaje =  "Archivo {} creado correctamente.".format(nombre)
    return mensaje

#Renombrar
def renombrar(nombre_viejo, nombre_nuevo, direccion_padre):
    mensaje = ""
    direccion = os.path.join(direccion_padre, nombre_nuevo)
    if os.path.exists(direccion):
        mensaje = "Ya hay otro archivo en la carpeta con ese nombre."
    else:
        os.rename(nombre_viejo, nombre_nuevo)
        if os.path.exists(direccion):
            mensaje = "Archivo renombrado exitosamente"
    return mensaje
    
#Mover una carpeta
def mover_carpeta(ruta_origen, ruta_destino, nombre):
    mensaje = ""
    origen = os.path.join(ruta_origen,nombre)
    destino = os.path.join(ruta_destino, nombre)
    if os.path.exists(destino):
        mensaje="no puede moverse la carpeta, ya hay una carpeta con ese nombre en el destino"
    else:
        shutil.copytree(origen, destino)
        if os.path.exists(destino):
            mensaje = "La carpeta se movió exitosamente"
    return mensaje
    ####
    #Falta borrar la carpeta
    ####
    

if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug=True)