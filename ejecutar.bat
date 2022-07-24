@echo off
REM permite utilizar los signos de admiración en lugar de los porcentajes
setlocal enabledelayedexpansion 
set extensionArchivoAOcultar=%1
CLS
:MENU
ECHO.
ECHO ...............................................
ECHO PRESIONE 1, 2 PARA SELECCIONAR UNA TAREA, O 3 PARA SALIR.
ECHO ...............................................
ECHO.
ECHO 1 - Ocultar todo
ECHO 2 - Desocultar todo
ECHO 3 - SALIR
ECHO.

SET /P M=Digite 1, 2 o 3, luego presione ENTER:
IF %M%==1 GOTO ocularTodo
IF %M%==2 GOTO desocularTodo
IF %M%==3 GOTO EOF

:ocularTodo
SET count=1
echo: 
@echo %time% -- INICIA el procesamiento de los archivos con la extension indicada
echo:
FOR /F "tokens=* USEBACKQ" %%F IN (`dir /b *.%extensionArchivoAOcultar%`) DO (
python3 ocul.py subir "paisaje !count!.jpg" %%F todo
SET /a count=!count!+1
)
echo:
@echo %time% -- FINALIZA el procesamiento de los archivos con la extension indicada
echo: 
pause
GOTO MENU

:desocularTodo
python3 ocul.py desocultarTodo noAplica
echo Se eliminara el archivo json, los archivos ofuscadores se eliminaron, se hace respaldo en temp
pause
mkdir temp
del temp\ofuscadores.json
copy ofuscadores.json temp
del ofuscadores.json
GOTO MENU