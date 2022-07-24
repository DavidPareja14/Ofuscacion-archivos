import sys
from cryptography.fernet import Fernet
'''
Programa que permite encriptar y desencriptar un archivo con el cifrado o encriptación en reposo
de Fernet

Ejecución:
python3 encriptarDesencriptar.py ofuscadores.json Encriptar/Desencriptar
'''

'''
Carga el contenido de una llave con la cual se ha hecho la encriptación de un archivo
'''
def cargarLlave():
    return open("key.key", "rb").read() #Opens the file, reads and returns the key stored in the file

'''
A partir de la acción enviada, se puede encriptar o desencriptar un archivo, si se intenta desencriptar con
una llava que no se utilizó para la encriptación, se lanza la excepción.
contenidoBinarioAEncriptar: es el contenido de un archivo encriptado o que se quiere desencriptar
'''
def encriptarOdesencriptar(contenidoBinarioAEncriptar, operacion):
	f = Fernet(cargarLlave())
	if operacion == "Encriptar":
		print("Encriptando archivo ... ")
		return f.encrypt(contenidoBinarioAEncriptar)
	elif operacion == "Desencriptar":
		print("desncriptando archivo ... ")
		return f.decrypt(contenidoBinarioAEncriptar)
	else:
		return contenidoBinarioAEncriptar

'''
Se encarga de cargar el contenido del archivo para el cual se va a realizar la operación de encriptación
o desencriptación.
'''
def cargarContenidoArchivo(nombreArchivoCifrar, operacion):
	try:
		with open(nombreArchivoCifrar, 'rb') as f2:
			contenidoArchivoOriginal = f2.read()
		with open(nombreArchivoCifrar, "wb") as f1:
			f1.write(encriptarOdesencriptar(contenidoArchivoOriginal, operacion))
	except:
		print("Hubieron errores")

nombreArchivoCifrar = sys.argv[1]
operacion = sys.argv[2]
print("Empezando ...")
cargarContenidoArchivo(nombreArchivoCifrar, operacion)