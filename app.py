from flask import Flask, redirect
import os

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
    #string_directrios = str(lista_directorios)
    #return string_directrios
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


if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug=True)