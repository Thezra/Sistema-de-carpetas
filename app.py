from flask import Flask, redirect
import os, shutil, stat

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

    
#Crear una nueva carpeta
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

#Crear un nuevo archivo
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

#Renombrar un archivo y carpeta
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
        mensaje="No puede moverse la carpeta, ya hay una carpeta con ese nombre en el destino"
    else:
        shutil.copytree(origen, destino)
        if os.path.exists(destino):
            mensaje = "La carpeta se movió exitosamente"
        eliminarCarpeta(nombre)
    return mensaje
    
#Copiar una carpeta
def copiar_carpeta(ruta_origen, ruta_destino, nombre):
    mensaje = ""
    origen = os.path.join(ruta_origen,nombre)
    destino = os.path.join(ruta_destino, nombre)
    if os.path.exists(destino):
        mensaje="No puede moverse la carpeta, ya hay una carpeta con ese nombre en el destino"
    else:
        shutil.copytree(origen, destino)
        if os.path.exists(destino):
            mensaje = "La carpeta se movió exitosamente"
    return mensaje

#Copiar un archivo 
def copiar_archivo(ruta_origen, ruta_destino, nombre):
    origen = os.path.join(ruta_origen,nombre)
    destino = os.path.join(ruta_destino, nombre)
    if os.path.exists(destino):
        nombre = "copia de "+nombre
        destino = os.path.join(ruta_destino, nombre)
        shutil.copy(origen, destino)
        shutil.copymode(origen, destino)
    else:
        shutil.copy(origen, destino)
        shutil.copymode(origen, destino)
    return "Archivo copiado"

#Eliminar archivo
def eliminarArchivo(nombre):
    os.remove(nombre)
    return "El archivo ha sido eliminado"

#Eliminar carpeta y TODO el contenido
def eliminarCarpeta(nombre):
    shutil.rmtree(nombre)
    return "La carpeta y todo su contenido han sido eliminados"

#Cambiar los permisos de un archivo o carpeta(sin afectar el contenido)
def cambiar_permisos(ruta_padre, nombre, num_permisos):
    ruta = os.path.join(ruta_padre,nombre)
    decimal = int(str(num_permisos), 8)
    os.chmod(ruta, decimal)
    return "Los permisos han sido cambiados correctamente"
    #NOTITA IMPORTANTE: Diferenciar entre permisos en recursividad o solo al archivo o carpeta actual <3 --- Listo

#Cambiar los permisos de una carpeta afectando el contenido
def cambiar_permisos_recursivo(nombre, num_permisos):
    comando = 'chmod -R '+str(num_permisos)+' '+nombre
    os.system(comando)
    mensaje = "Permisos de la carpeta actualizados exitosamente"
    return mensaje

#NO PETAN, PERO TAMPOCO FUNCIONAN XD:

#Cambiar el usuario dueño de solo ese archivo
def cambiar_dueño(nuevo_dueño, nombre):
    comando = 'sudo chown '+nuevo_dueño+' '+nombre
    sudo_password = "danalejo+02"
    os.system('echo %s|sudo -S %s' % (sudo_password, comando))
    mensaje = "Usuario dueño del archivo actualizado correctamente"
    return mensaje
    #NOTITA IMPORTANTE: Poner en "sudo_password" tu contraseña de ubuntu

#Cambiar el usario dueño de una carpeta y su contenido
def cambiar_dueño_recursivo(nuevo_dueño, nombre_carpeta):
    sudo_password = "danalejo+02"
    comando = 'chown -R'+nuevo_dueño+' '+nombre_carpeta
    os.system('echo %s|sudo -S %s' % (sudo_password, comando))
    mensaje = "Dueño actualizado correctamente"
    return mensaje
    #NOTITA IMPORTANTE: Poner en "sudo_password" tu contraseña de ubuntu



if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug=True)
