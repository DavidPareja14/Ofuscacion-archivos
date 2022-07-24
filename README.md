# Ofuscacion-archivos
El proyecto es creado con el fin de ocultar archivos desde la línea de comandos, se puede ofuscar un archivo individual pasando la imagen con la que se desea ofuscar o se puede ejecutar un batch para ocultar automáticamente todos los archivos en un directorio según la extensión de archivos enviada como argumento.

## Proceso
Es posible que en una carpeta tengamos muchos vídeos, fotos o cualquier tipo de archivo, por lo que sería dispendioso tomar cada nombre de archivo y una imagen para encriptar uno por uno, por lo que en este caso lo mejor sería utilizar el archivo ejecutar.bat, para esto, nos ubicamos con línea de comandos en la carpeta en donde están los archivos y ejecutamos

>ejecutar nombreExtensionArchivo

Con lo anterior, se nos presenta un menú con tres opciones:
* la primera sirve para ocultar todos los archivos con la extensión anteriormente indicada, si es la primera vez que se ejecuta el programa, se creará un archivo llamado key, el cuál es una clave simétrica creada a través del algoritmo de Fernet, todos los archivos a ofuscar estarán encriptados con la llave creada, por lo que al tratarse de una llave simétrica, es indispensable que este archivo (key) sea guardado en un lugar seguro para luego poder desencriptar los archivos. 
* La segunda opción, consiste en mostrar todos los archivos según la extensión indicada, acá es fundamental que en el directorio en donde se van a desencriptar los archivos, esté el archivo key, esto es por que de otra forma, no se podrá desencriptar los archivos y es posible que se puedan perder, por lo que nuevamente, hay que guardar muy bien el archivo key y siempre ubicarlo en la carpeta al querrer ocultar o desocultar y luego volver a guardar en otra ubicación el archivo key.
* La tercera opción es para salir de la aplicación.

Una vez ocultados todos los archivos, se crea un archivo ofuscadores.json, este archivo guarda un par clave - valor con el fin de guardar los nombres de los archivos como originalmente estaban junto con su tamaño e identificar el nombre del archivo ofuscador con el respectivo hash para que así se cree una clave única. Lo aconsejable es utilizar el archivo ***encriptarDesencriptar*** con el archivo key generado para encriptar el archivo ofuscadores.json y así no revelar el contenido, la encriptación se puede lograr ejecutando:

>python3 encriptarDesencriptar.py ofuscadores.json Encriptar

Del mismo modo, a la hora de desocultar archivos ofuscadores.json se debe desencriptar, para esto se ejecuta:
>python3 encriptarDesencriptar.py ofuscadores.json Desencriptar

### Ocultar archivo por archivo
Es posible que solo queramos ocultar un archivo, para esto, podemos ejecutar:
>python3 ocul.py subir "nombre archivo ofuscador" nombreArchivo.extension cualquierCosa

El nombre de archivo ofuscador puede ser el nombre de un archivo que sería una imagen, por ejemplo, imagen1.jpg, seguidamente está el nombre del archivo que deseamos encriptar y el tercer argumento puede ser cualquier texto, esto permite saber al programa si se está ejecuntado desde ejecutar.bat o archivo por archivo, acá hay que tener en cuenta las mismas consideraciones con el archivo key mencionado anteriormente.

Es importante aclarar que el programa está creado con ***python 3.9*** y funciona solo para windows desde el símbolo del sistema.
