import os
import sys
import json
import hashlib
from PIL import Image, ImageEnhance
import random
from cryptography.fernet import Fernet

'''
Este código se puede ejecutar desde dos partes, la primera es directamente, es decir, entrando por línea
de comandos hasta la ruta de este archivo y ejecutar python3 programa.py operacion archivoOfuscador archivoOcultar indicador
El archivoOcultar y el indicador solo es para cuando se van a subir archivos:
	archivoOcultar: es el archivo que se desea ocultar, puede ser cualquier tipo
	indicador: Si es todo, significa que se va a ejecutar desde el batch ejecutar.bat, de lo contrario, si es directamente
			   Puede poner cualquier valor.

Si se va a utilizar ejecutar.bat, este para que pueda tomar la extensión del archivo o en este caso, de los archivos a
ocultar, no se puede dar doble clic sobre el ejecutable, se debe ejecutar desde cmd, así:
	ejecutar extensionArchivosOcultar
El programa ejecutable ya sabe como llamar al programa de python3, hay que tener en cuenta que este concatena un hash
al archivo ofuscador, ese hash corresponde al contenido del archivo ofuscador con el archivo a ocultar.
Si en el programa ejecutable se selecciona desocultar todo, lo que pasa es que se recuperan los archivos ocultos que es-
tán en un JSON ofuscadores.json, ENTONCES se elimina los archivos ofuscadores y el archivo ofuscadores.json una vez
se hayan recuperado los archivos ocultos.

Si se va a ofuscar todos los archivos según una extensión de archivo, se toma como base NOMBRE_ARCHIVO que representa
el nombre de un archivo de una imagen, este archivo como tal no se utilizará para ofuscar sino para crear nuevas imágenes
las cuales si van a ofuscar.
Si se ejecuta el programa para ofuscar un archivo específico, se debe pasar el nombre del archivo ofuscador, este no influye
para generar otros archivos ofuscadores.

Ejemplos:
Archivo individual:
python3 ocul.py subir "nombre archivo ofuscador" detalle_de_compra.pdf cualquierCosa
python3 ocul.py bajar nombreArchivo --->   TENER EN CUENTA que no se puede utilizar el nombre que está en NOMBRE_ARCHIVO,
									pero ese nombreArchivo, es en realidad el nombre de la clave con que se guardó ese
									archivo en ofuscadores.json

Si se va a ejecutar para ocultar todo:
	ejecutar extensionArchivo
Si solo se va a desocultar, no es necesario la extension del archivo.

NOTA:
Si se va a ejecutar el ejcutar.bat, es mejor que todos los archivos con la extensión indicada, no tengan espacios
o caracteres especiales, ya que si tienen espacios, esto entrará como parámetro a python, pero por cada espacio, 
se tomará como un argumento diferente y puede tomarse los datos como no son.
 además, al desocultar todo, se eliminan los archivos ofuscadores, hasta los que se ofuscaron
sin el ejecutar.bat

ADVERTENCIA
NO SUBIR ARCHIVOS QUE LOS NOMBRES TENGAN ESPACIOS, ESTO HARÁ QUE NO SE PUEDAN REFERENCIAR EN ofuscadores.json y lo
peor es que puede que hayan quedado archivos ofuscados y ya no se puedan recuperar
Siempre verificar que en el archivo ofuscadores.json estén los archivos que deban estar.

EJECUTAR ANTES:
Hay varias key o llaves para desencriptar, solo yo sé cual es la que sirve, si se usa la que no es, se eliminarán los archivos.
'''

NOMBRE_ARCHIVO = "paisaje1.jpg"

def write_key():
    key = Fernet.generate_key() # Generates the key
    with open("key.key", "wb") as key_file: # Opens the file the key is to be written to
        key_file.write(key) # Writes the key

def load_key():
    return open("key.key", "rb").read() #Opens the file, reads and returns the key stored in the file

'''
A partir de la acción enviada, se puede encriptar o desencriptar un archivo, si se intenta desencriptar con
una llava que no se utilizó para la encriptación, se lanza la excepción.
'''
def encriptarOdesencriptar(contenidoBinarioAEncriptar, operacion):
	f = Fernet(load_key())
	if operacion == "Encriptar":
		return f.encrypt(contenidoBinarioAEncriptar)
	elif operacion == "Desencriptar":
		return f.decrypt(contenidoBinarioAEncriptar)

'''
Método encargado de crear una llave de encriptación y desencriptación en caso de que no exista, 
además, permite manejar los errores que surja al desncriptar el archivo.
'''
def coordinarEncriptacionDesencriptacion(contenidoBinarioAEncriptar, operacion):
	try:
		#Si no existe el archivo que contiene la llave, se lanza excepción y se crea llave
		return encriptarOdesencriptar(contenidoBinarioAEncriptar, operacion)
	except FileNotFoundError as fnf:
		print("Se creará la clave simétrica: {0}".format(fnf))
		write_key()
		return encriptarOdesencriptar(contenidoBinarioAEncriptar, operacion)
	except Exception as ex:
		print("LOG --> Si está desencriptando, puede que se esté utilizando llave incorrecta: {0}".format(ex))
		return b"No se pudo desencriptar"

'''
Se realiza la ofuscación de un archivo, posteriormente, se elimina el archivo que se va a ocultar
'''
def ofuscarArchivo():
	try:
		with open(archivoOfuscador, "ab") as f:
			with open(archivoOcultar, 'rb') as incrustar:
				f.write(coordinarEncriptacionDesencriptacion(incrustar.read(), "Encriptar"))
		os.remove(archivoOcultar)
	except FileNotFoundError as fnfe:
		raise NameError('NoExisteArchivoOfuscadorOArchivoOcultar')

'''
Dado el nombre del archivo, se verifica si este está almacenado en 
el diccionario de archivos ofuscadores
diccionario: diccionario JSON con las claves y valores
nombreArchivo: es el nombre del archivo a buscar en el diccionario
'''
def verificarArchivoDiccionario(diccionario, nombreArchivo):
	existeNombreArchivo = True
	if nombreArchivo in diccionario:
		print("No se puede utilizar el archivo ofuscador")
		return existeNombreArchivo
	return not existeNombreArchivo

'''
Permite abrir el archivo ofuscadores.json en caso de existir, de lo contrario se genera una excepción, esto sucede
si es la primera vez que se van a ocultar archivos, para desocultar, esto no debe de suceder.
'''
def abrirDiccionario():
	with open("ofuscadores.json") as archivoOfuscadores: 
		diccionarioOfuscadores=json.load(archivoOfuscadores)
		archivoOfuscadores.close()
	return diccionarioOfuscadores

'''
Permite sobreescribir el archivo de ofuscadores para almacenar nuevos archivos ocultos o para ya no tener
en cuenta archivos ofuscadores dado que ya no están ocultando archivos.
'''
def guardarDiccionario(diccionario):
	files = open("ofuscadores.json", "w") 
	json.dump(diccionario, files)
	files.close()

'''
En el archivo ofuscadores.json se agrega una nueva entrada al diccionar para que se establezca cual es el
archivo ofuscador que oculta otro archivo, se almacena el archivo a ocultar ocn el tamaño del archivo ofuscador.
Si no existe el archivo ofuscador, no se oculta el archivo y no se guarda en el ofuscadores.json
'''
def adicionarArchivoOfuscador():
	'''
	Si un archivo es subido con espacios, entonces se van a interpretar más argv o argumentos de los que se
	debe y indicadarTodoIndividual puede ser otra cosa, por lo que esto puede hacer que se lea un archivo que no
	existe de carpeta, por ejemplo, paisaje 2.jpg, ya que los nombres de archivos cuando el indicador es todo se
	GENERAN AUTOMÁTICAMENTE, si ese indicador se manda todo, pero a la final hay más argumentos, el indicador
	no se tomará en realidad, se tomará otro nombre, esto lo debería manejar con una excepción
	'''
	try:
		tamanoArchivoOfuscador = os.stat(archivoOfuscador).st_size
	except FileNotFoundError as fallo:
		print("ERROR: si un archivo tiene espacios, se pasan más argumentos por línea de comandos de los que se deben, esto haría que indicadarTodoIndividual no se lea como es y que el programa no se ejecute como todo sino como si quisiera subir archivo por archivo")
	print("LOG --> Se obutuvo tamaño archivo ofuscador")
	try:
		diccionarioOfuscadores = abrirDiccionario()
		print("LOG --> Se pudo abrir diccionario ofuscadores")
		if not verificarArchivoDiccionario(diccionarioOfuscadores, archivoOfuscador):
			diccionarioOfuscadores[archivoOfuscador]=archivoOcultar + "---" + str(tamanoArchivoOfuscador)
			ofuscarArchivo()
			print("LOG --> Se pudo ocultar el archivo")
			guardarDiccionario(diccionarioOfuscadores)
			print("LOG --> Se pudo guardar el didccionario con el nuevo ofuscador")
	except FileNotFoundError as fnfe:
		ofuscarArchivo()
		print("LOG --> Se pudo ocultar el archivo")
		print("LOG --> El archivo de ofuscadores no existe: {0}".format(fnfe))
		guardarDiccionario({archivoOfuscador: archivoOcultar + "---" + str(tamanoArchivoOfuscador)})
		print("LOG --> Se crea el archivo JSON con los ofuscadores y adición del nuevo ofuscador")
	except NameError as ne:
		print("LOG --> No se encuentra el archivo ofuscador, NO SE OCULTA EL ARCHIVO, PUEDE que tenga espacios el nombre del archivo a ocultar: {0}".format(ne))

'''
Se recupera el archivo oculto
nombreArchivoOculto: nombre del archivo que ha estado oculto, este nombre se le pone al archivo
tamanoArchivoOfuscador: tamaño del archivo ofuscador necesario para determinar desde donde se toma el archivo oculto
paramArchivoOfuscador: Es el nombre del archivo ofuscador
'''
def recuperarArchivoOculto(nombreArchivoOculto, tamanoArchivoOfuscador, paramArchivoOfuscador):
	print("ArchivoOculto: " + nombreArchivoOculto + "Tamaño: " +  tamanoArchivoOfuscador + "archivoOfuscador: " + paramArchivoOfuscador)
	with open(paramArchivoOfuscador, "rb") as f:
		with open(nombreArchivoOculto, 'wb') as incrustar2:
			f.seek(int(tamanoArchivoOfuscador), 1) #tomo lo que haya después de la cantidad de bytes.
			incrustar2.write(coordinarEncriptacionDesencriptacion(f.read(), "Desencriptar"))	

'''
En esta parte, se elimina de ofuscadores.json el archivo o clave del archivo ofuscador dado que este ya no 
ocultará archivos, pero como se puede ocultar todo o se puede ocultar un archivo específico, hay que determinar
si el archivo ofuscador se elimina del explorador de archivos, ya que la metodología es diferente.
Si todos los archivos se van a ocultar, solo se necesita un archivo ofuscador y en base a este se crean más archivos 
ofuscadores.
Si se va a ocultar un archivo directamente, puede pasar el nombre del archivo ofuscador y este será el único archivo 
ofuscador de su tipo, el programa no lo genera, por eso este archivo no es viable eliminarlo.
'''
def eliminarArchivoOfuscador(diccionarioOfuscadores, paramArchivoOfuscador, temp):
	nombreArchivoOculto, tamanoArchivoOfuscador = diccionarioOfuscadores[paramArchivoOfuscador].split("---")
	recuperarArchivoOculto(nombreArchivoOculto, tamanoArchivoOfuscador, paramArchivoOfuscador)
	#Se elimina el nombre de archivo ofuscador del diccionario para que luego pueda ocultar otro archivo
	if temp == "noAplica":
		pass
	else:
		del diccionarioOfuscadores[paramArchivoOfuscador]
		guardarDiccionario(diccionarioOfuscadores)
	#Se deja el archivo ofuscador original y se recupera el archivo oculto, aunque luego opto por eliminarlo,lo dejo por si algo
	with open(paramArchivoOfuscador, 'rb') as f2:
		contenidoArchivoOriginal = f2.read(int(tamanoArchivoOfuscador))
	with open(paramArchivoOfuscador, "wb") as f1:
		f1.write(contenidoArchivoOriginal)
	os.remove(paramArchivoOfuscador)

'''
Permite determinar si se está ejecutando ejecutar.bat, este lanza la operación desocultarTodo,
si la operación es bajar, es porque se está tratando desocultar solo un archivo.
Para desocultar todo, no es necesario tener el archivo ofuscadores.json, por lo tanto se puede eliminar luego
de sacar los archivos.
Para desocultar un archivo, simplemente se elimina la entrada en el diccionar para el archivo ofuscador.
'''
def modoRecuperacionArchivoOriginal(operacion, ofuscador):
	diccionarioOfuscadores = abrirDiccionario()
	if operacion == "bajar":
		eliminarArchivoOfuscador(diccionarioOfuscadores, ofuscador, ofuscador)
	elif operacion == "desocultarTodo":
		for nombreOfuscador in diccionarioOfuscadores.keys():
			eliminarArchivoOfuscador(diccionarioOfuscadores, nombreOfuscador, ofuscador)

'''
Metodo encargado de retornar el hash relacionado al nombre supuesto de un archivo
'''
def hashArchivo(nombreArchivo):
	#print(nombreArchivo)  SE COMENTA por si necesito sacar el hast del contenido de un archivo
	#sha1 = hashlib.sha1()
	#hashe = ""
	#with open(nombreArchivo, "rb") as archi:
		#sha1.update(archi.read())
		#hashe = sha1.hexdigest()
	print(nombreArchivo)
	sha1 = hashlib.sha1()
	hashe = ""
	sha1.update(nombreArchivo.encode("utf-8"))
	hashe = sha1.hexdigest()
	return hashe

'''
A partir del nombre de archivo NOMBRE_ARCHIVO se genrarán más imágenes con 
constastes diferentes para cada archivo que se quiera ocultar.
'''
def crearImagenOfuscadora(archivoOfuscador):
	#read the image
	im = Image.open(NOMBRE_ARCHIVO)

	#image brightness enhancer
	enhancer = ImageEnhance.Contrast(im)

	factor = random.random() #gives original image
	im_output = enhancer.enhance(factor * 5.0)
	im_output = im_output.rotate(factor * 360)
	archivoOfuscadorNombre, ext = archivoOfuscador.split(".")
	archivoOfuscadorNuevo = archivoOfuscadorNombre + "-" + hashArchivo(archivoOfuscador + archivoOcultar) + "." + ext 
	im_output.save(archivoOfuscadorNuevo)
	return archivoOfuscadorNuevo

from time import time
time_ini = time()
operacion = sys.argv[1]
archivoOfuscador = sys.argv[2]
#print(hashArchivo(archivoOfuscador))
#crearImagenOfuscadora(archivoOfuscador)
if operacion == "subir":
	archivoOcultar = sys.argv[3]
	indicadarTodoIndividual = sys.argv[4]
	if indicadarTodoIndividual == "todo":
		#Evito que se oculte el archivo que se usa para crear archivos ofuscadores.
		if archivoOcultar != NOMBRE_ARCHIVO:
			archivoOfuscador = crearImagenOfuscadora(archivoOfuscador)
			adicionarArchivoOfuscador()
	elif archivoOfuscador == NOMBRE_ARCHIVO:
		print("No se puede utilizar el archivo ofuscador, usado para otro fin")
	else:
		adicionarArchivoOfuscador()
else:
	modoRecuperacionArchivoOriginal(operacion, archivoOfuscador)

time_fin = time()
tiempoTranscurrido = time_fin - time_ini
print("Tiempo para archivo: " + archivoOfuscador + " --> " + str(tiempoTranscurrido))