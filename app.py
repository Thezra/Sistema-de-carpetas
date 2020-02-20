from flask import Flask, redirect, render_template, request
import os, shutil, stat, subprocess, funciones

#NOTA IMPORTANTE: Cambiar en las 3 líneas que aparece /home/thera por /home/(su nombre de usuario)

app = Flask(__name__)
#app.secret_key = "peo"
Ruta = "/home/daniel/"
NombreArchivo = ""
RutaOrigen = ""
    

#Para "subir" a la pagina anterior
@app.route('/atras')
def quitar_a_ruta():
    global Ruta
    if Ruta == "/home/daniel/":
        return mostrar_contenido_carpeta(Ruta)
    else:
        ruta = Ruta.split("/")
        ruta.pop(-1)
        ruta.pop(-1)
        ruta_nueva =""
        for i in ruta:
            ruta_nueva = ruta_nueva+i+"/"
        Ruta = ruta_nueva
        return mostrar_contenido_carpeta(ruta_nueva)

@app.route('/actualizar')
#Para "actualizar" la ruta
def actualizar_pagina():
    global Ruta
    return mostrar_contenido_carpeta(Ruta)

#Para "bajar" en la ruta
def agregar_a_ruta(nombre_carpeta ):
    global Ruta
    Ruta = Ruta+str(nombre_carpeta)+"/"
    return Ruta

#def generar_ruta(nombre):
#    #return os.system("realpath "+nombre)
#    return os.path.realpath(nombre)
#    #return str(nombre)


@app.route('/')
def inicio():
    return redirect('/Home')


#muestra la carpeta home automaticamente al inicar
@app.route('/Home')
def mostrar_home():
    contenido = os.path.expanduser('~')
    global Ruta
    Ruta = "/home/daniel/"
    lista_dir = []
    lista_archivos = []
    lista_directorios = os.listdir(contenido)
    for i in lista_directorios:
        if os.path.isdir(Ruta+i):
            if i[0]!=".":
                lista_dir.append(i)
        elif os.path.isfile(Ruta+i):
            if i[0]!=".":
                lista_archivos.append(i)
    return render_template("index.html", listadir=lista_dir, listaarch=lista_archivos)

    #return str(lista_archivos)

#Muestra el contenido de la carpeta
@app.route('/Mostrar_Carpeta', methods=['GET'])
def mostrar_contenido_carpeta(back=""):
    lista_dir = []
    lista_archivos = []
    if back == "":
        carpeta = request.args.get('carpeta')
        carpeta = str(carpeta).strip("'")
        ruta = agregar_a_ruta(carpeta)
    else:
        ruta=back

    lista_directorios = os.listdir(ruta)
    for i in lista_directorios:
        if os.path.isdir(Ruta+i):
            if i[0]!=".":
                lista_dir.append(i)
        elif os.path.isfile(Ruta+i):
            if i[0]!=".":
                lista_archivos.append(i)
    return render_template("index.html", listadir=lista_dir, listaarch=lista_archivos)


#Muestra el contenido de la carpeta (version paralela 1)
@app.route('/Mostrar_Carpeta1', methods=['GET'])
def mostrar_contenido_carpeta1(back=""):
    lista_dir = []
    if back == "":
        carpeta = request.args.get('carpeta')
        carpeta = str(carpeta).strip("'")
        ruta = agregar_a_ruta(carpeta)
    else:
        ruta=back

    lista_directorios = os.listdir(ruta)
    for i in lista_directorios:
        if os.path.isdir(Ruta+i):
            if i[0]!=".":
                lista_dir.append(i)
    return render_template("copiar.html", listadir=lista_dir)


#muestra la carpeta home automaticamente al inicar
#@app.route('/Home')
#def mostrar_home():
#    lista_archivos = mostrar_contenido_carpeta("~")
#    return render_template("index.html", lista=lista_archivos)
#    return crear_carpeta("peo", "~")

#Muestra el contenido de la carpeta
#def mostrar_contenido_carpeta(carpeta):
#    home = os.path.expanduser(carpeta)
#    lista_directorios = os.listdir(home)
#    return lista_directorios

#Crear una nueva carpeta
'''def crear_carpeta(nombre, direccion_padre):
    direccion = os.path.join(direccion_padre, nombre)
    permisos = 0o770
    if os.path.exists(direccion):
        mensaje = "La carpeta no puede crearse, ya existe."
    else:
        os.mkdir(direccion, permisos)
        if os.path.exists(direccion):
            mensaje =  "Carpeta {} creada correctamente.".format(nombre)
    return mensaje'''

#Crea carpeta llamando a la funcion
@app.route("/crear_carpeta", methods=["POST", "GET"])
def crear_dir():
    global Ruta
    if request.method == "POST":
        nombre = request.form["Nombre_carpeta"]
        direccion_padre = Ruta

    return funciones.crear_carpeta(nombre, direccion_padre)

#Crear un nuevo archivo
'''def crear_archivo(nombre,direccion_padre):
    direccion = os.path.join(direccion_padre, nombre)
    permisos = 0o740
    mensaje = ""
    if os.path.exists(direccion):
        mensaje = "El archivo no puede crearse, ya existe."
    else:
        os.open(nombre, permisos)
        if os.path.exists(direccion):
            mensaje =  "Archivo {} creado correctamente.".format(nombre)
    return mensaje'''

#Creación de archivo llamando a la función   
@app.route("/crear_archivo", methods=["POST", "GET"])
def crear_file():
    global Ruta
    if request.method == "POST":
        nombre = request.form["Nombre_archivo"]
        direccion_padre = Ruta
    return funciones.crear_archivo(nombre, direccion_padre)

#Renombrar un archivo o carpeta
'''@app.route("/renombrar",  methods=["POST"])
def renombrar():
    global Ruta
    nombre_viejo = request.form["nombre_viejo"]
    nombre_nuevo = request.form["nombre_nuevo"]
    os.rename(Ruta+nombre_viejo, Ruta+nombre_nuevo)
    if os.path.exists(Ruta+nombre_nuevo):
        return actualizar_pagina()'''

@app.route("/renombrar",  methods=["POST"])
def renombrar():
    global Ruta
    nombre_viejo = request.form["nombre_viejo"]
    nombre_nuevo = request.form["nombre_nuevo"]
    mensaje_error = "No se ha podido renombrar"
    try:
        os.rename(Ruta+nombre_viejo, Ruta+nombre_nuevo)
        return actualizar_pagina()
    except OSError:
        return render_template("error.html", mensaje=mensaje_error)

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
    
#Boveda_copiado
@app.route("/boveda", methods=['POST'])
def boveda_temporal():
    global NombreArchivo
    global RutaOrigen
    global Ruta
    lista_dir=[]
    NombreArchivo = request.form['nombre']
    RutaOrigen = os.path.join(Ruta,NombreArchivo)
    ruta = Ruta.split("/")
    ruta.pop(-1)
    ruta.pop(-1)
    ruta_nueva =""
    for i in ruta:
        ruta_nueva = ruta_nueva+i+"/"
    Ruta = ruta_nueva
    lista_directorios = os.listdir(Ruta)
    
    for i in lista_directorios:
        if os.path.isdir(Ruta+i):
            if i[0]!=".":
                lista_dir.append(i)
    
    return render_template("copiar.html", listadir = lista_dir)

#Copiar una carpeta
@app.route("/copiar_carpeta")
def copiar_carpeta():
    global Ruta
    global NombreArchivo
    global RutaOrigen


    dest = os.path.join(Ruta, NombreArchivo)
    #origen = os.path.join(RutaOrigen, NombreArchivo)
    
    shutil.copytree(RutaOrigen, dest)
    return mostrar_home()
    #if os.path.exists(destino):
    #    mensaje = "No puede moverse la carpeta, ya hay una carpeta con ese nombre en el destino"
    #else:
    #    shutil.copytree(origen, destino)
    #    if os.path.exists(destino):
    #        mensaje = "La carpeta se movió exitosamente"
    #return mensaje

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
@app.route("/eliminar_archivo", methods=["POST"])
def eliminarArchivo():
    global Ruta
    nombre = request.form["nombre_archivo"]
    direccion = Ruta+nombre
    os.remove(direccion)
    return actualizar_pagina()

#Eliminar carpeta y TODO el contenido
@app.route("/eliminar_carpeta", methods=["POST"])
def eliminarCarpeta(back=""):
    global Ruta
    if back=="":
        nombre = request.form["nombre_archivo"]
    else:
        nombre=back
    mensaje_error = "No se ha podido eliminar la carpeta"
    try:
        shutil.rmtree(Ruta+nombre)
        return actualizar_pagina()
    except OSError:
        return render_template("error.html", mensaje=mensaje_error)


#Cambiar los permisos de un archivo o carpeta(sin afectar el contenido)
'''def cambiar_permisos(ruta_padre, nombre, num_permisos):
    ruta = os.path.join(ruta_padre,nombre)
    decimal = int(str(num_permisos), 8)
    os.chmod(ruta, decimal)
    return "Los permisos han sido cambiados correctamente"'''
    #NOTITA IMPORTANTE: Diferenciar entre permisos en recursividad o solo al archivo o carpeta actual <3 --- Listo

@app.route("/cambiar_permisos", methods=["POST"])
def cambiar_permisos():
    global Ruta
    nombre = request.form["nombre"]

    usuario_l = int(request.form["user_r"])
    usuario_es = int(request.form["user_w"])
    usuario_ej = int(request.form["user_x"])

    grupo_l = int(request.form["grupo_r"])
    grupo_es = int(request.form["grupo_w"])
    grupo_ej = int(request.form["grupo_x"])

    otros_l = int(request.form["otros_r"])
    otros_es = int(request.form["otros_w"])
    otros_ej = int(request.form["otros_x"])

    num_permisos = str(usuario_l+usuario_es+usuario_ej)+str(grupo_l+grupo_es+grupo_ej)+str(otros_l+otros_es+otros_ej)

    decimal = int(num_permisos, 8)
    os.chmod(Ruta+nombre, decimal)
    mensaje = "Los permisos han sido cambiados correctamente"
    return render_template("exito.html", mensaje=mensaje)

#Cambiar los permisos de una carpeta afectando el contenido
'''@app.route("/cambiar_permisos_recursivo", methods=["POST"])
def cambiar_permisos_recursivo():
    global Ruta
    sudo_password = request.form["sudo_password"]
    nombre = request.form["nombre"]
    usuario_l = int(request.form["user_r"])
    usuario_es = int(request.form["user_w"])
    usuario_ej = int(request.form["user_x"])
    grupo_l = int(request.form["grupo_r"])
    grupo_es = int(request.form["grupo_w"])
    grupo_ej = int(request.form["grupo_x"])
    otros_l = int(request.form["otros_r"])
    otros_es = int(request.form["otros_w"])
    otros_ej = int(request.form["otros_x"])
    mensaje_exito = "Permisos de la carpeta y todo su contenido actualizados exitosamente"
    mensaje_error = "No se han podido cambiar los permisos"
    num_permisos = str(usuario_l+usuario_es+usuario_ej)+str(grupo_l+grupo_es+grupo_ej)+str(otros_l+otros_es+otros_ej)
    comando = 'sudo chmod -R '+str(num_permisos)+' '+str(nombre)
    try:
        os.system('echo %s|sudo -S %s' % (sudo_password, comando))
        return render_template("exito.html", mensaje=mensaje_exito)
    except OSError:
        return render_template("error.html", mensaje=mensaje_error)'''


#Cambiar el usuario dueño de solo ese archivo
@app.route("/cambiar_owner", methods=["POST"])
def cambiar_owner():
    global Ruta
    sudo_password = request.form["sudo_password"]
    nuevo_owner = request.form["nuevo_owner"]
    nombre = request.form["nombre"]
    comando = 'sudo chown '+str(nuevo_owner)+' '+str(Ruta+nombre)
    mensaje_exito = "Usuario dueño del archivo actualizado correctamente"
    mensaje_error = "No se ha podido cambiar el dueño"
    try:
        os.system('echo %s|sudo -S %s' % (sudo_password, comando))
        return render_template("exito.html", mensaje=mensaje_exito)
    except OSError:
        return render_template("error.html", mensaje=mensaje_error)

#Cambiar el usario dueño de una carpeta y su contenido
@app.route("/cambiar_owner_recursivo", methods=["POST"])
def cambiar_owner_recursivo():
    global Ruta
    sudo_password = request.form["sudo_password"]
    nuevo_owner = request.form["nuevo_owner"]
    nombre = request.form["nombre"]
    comando = 'sudo chown -R '+nuevo_owner+' '+str(nombre+Ruta)
    mensaje_exito = "Usuario dueño del objeto y de todos sus hijos ha sido cambiado correctamente"
    mensaje_error = "No se ha podido cambiar el dueño"
    try:
        #os.system('echo %s|sudo -S %s' % (sudo_password, comando))
        os.system(comando)
        return render_template("exito.html", mensaje=mensaje_exito)
    except OSError:
        return render_template("error.html", mensaje=mensaje_error)
    #NOTITA IMPORTANTE: Poner en "sudo_password" tu contraseña de ubuntu

#Mostrar permisos de todos los archivos de una carpeta
'''def mostrar_permisos_global():
    #comando = "ls -l"
    #salida = os.system(comando)
    resultado = subprocess.getoutput("ls")
    #return str(resultado)
    lista_nombres = resultado.split("\n")
    string_para_return = ""
    for i in lista_nombres:
        permisos = mostrar_permisos_especifico(i)
        string_para_return = string_para_return+" "+permisos+"\n"
    return string_para_return '''

#Mostrar permisos de un archivo en especifico
@app.route("/mostrar_permisos", methods=["POST"])
def mostrar_perms():
    global Ruta
    nombre = request.form["nombre"]
    return funciones.mostrar_permisos(nombre, Ruta)

if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug=True)
