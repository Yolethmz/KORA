import speech_recognition as sr
import pyttsx3
import pymysql
from os import system

#horas invertidas = 35

error='Conexion Fallida y error de sintaxis'

listener = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen(texto):
    try:
        with sr.Microphone() as source:
            print(texto)
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language='es-ES')
            rec = rec.lower()
            print("Dijiste: " + rec)                                                
    except:
        pass

    return rec

def editDataBase(name,cond):
    try:
        miconexion=pymysql.connect(host="localhost",user="root",password="ASAS15",db="mysql")
        micursor=miconexion.cursor()
        talk('Conexion exitosa')

        if cond == True:
            #Creando base de datos
            micursor.execute("CREATE DATABASE IF NOT EXISTS "+name)
            talk("Base de datos creada correctamente")
        
        elif cond == False:
            #Eliminando base de datos
            micursor.execute("DROP DATABASE "+name)
            talk("Base de datos eliminada correctamente")

        #Cierre de conexion
        miconexion.commit()
        miconexion.close()
        micursor.close()

    except:
        talk(error)

def editTable(dataname, tablename, cond):
    try:
        #Ingresando a la base de datos "dataname"
        miconexion=pymysql.connect(host="localhost",user="root",password="ASAS15",db=dataname)
        micursor=miconexion.cursor()

        #Creando tablas en "dataname" y agregando una columna por defecto
        if cond == True:
            micursor.execute("CREATE TABLE IF NOT EXISTS "+tablename+"( defaultID INT(11) AUTO_INCREMENT, CONSTRAINT  default_pk PRIMARY KEY (defaultID) )")
            talk("Tabla creada correctamente")

        elif cond == False:
            micursor.execute("DROP TABLE "+tablename)
            talk("Tabla eliminada correctamente")

        #Cierre de conexion 
        miconexion.commit()
        miconexion.close()
        micursor.close()

    except:
        talk(error)
    
def EditColumn(dataname, tablename):
    try:
        #Ingresando a la base de datos "dataname"
        miconexion=pymysql.connect(host="localhost",user="root",password="ASAS15",db=dataname)
        micursor=miconexion.cursor()

        print('Opciones: crear columna, editar columna, eliminar columna')
        rec = listen('Esperando ordenes...')
        system("cls")

        if 'crear columna' in rec:
            talk('Por favor siga el siguiente formato')
            print('var_name var_type(var_long) extras')

            columnname = input('Valor: ')
            micursor.execute("ALTER TABLE "+tablename+" ADD ("+columnname+")")
            talk('Columna creada correctamente')
            
        elif 'editar columna' in rec:
            print('Opciones: modificar columna, renombrar columna')
            rec = listen('Esperando ordenes...')

            if 'modificar columna' in rec:
                talk('Por favor, ingrese los nuevos datos de la columna')
                print('Formato: var_name var_type(var_long) extras')

                newcolumn = input('Valor: ')
                micursor.execute("ALTER TABLE "+tablename+" MODIFY "+ newcolumn)
                talk('Columna modificada correctamente')


            elif 'renombrar columna' in rec:
                talk('Ingrese la columna a renombrar: ')
                oldcolumn = input('Valor: ')
                system('cls')

                talk('Por favor, ingrese los nuevos datos de la columna')
                print('Formato: var_name var_type(var_long) extras')

                newcolumn = input('Valor: ')

                micursor.execute("ALTER TABLE "+tablename+" CHANGE "+ oldcolumn + " " + newcolumn)
                talk('Datos modificados con exito')              

        elif 'eliminar columna' in rec:
            talk("Porfavor, ingrese la columna a eliminar")
            columnname = input("valor: ")
                                
            micursor.execute("ALTER TABLE "+tablename+" DROP "+columnname)
            talk("Columna eliminada correctamente")

        #Cierre de conexion
        miconexion.commit()
        miconexion.close()
        micursor.close()

    except:
        talk(error)

def InsertData(dataname, tablename):
    try:
        #Ingresando a la base de datos "dataname"
        miconexion=pymysql.connect(host="localhost",user="root",password="ASAS15",db=dataname)
        micursor=miconexion.cursor()

        #Establecer columna
        talk('Ingrese el nombre de la columna')
        columnname = input('Valor: ')

        #Datos en la columna
        talk('Ingrese el dato a ingresar en la columna')
        data = input('Valor: ')

        #Query
        micursor.execute("insert into "+tablename+"("+columnname+")"+" values('{}')".format(data))
        talk('Dato ingresado correctamente')
        
        #Cerrar conexion
        miconexion.commit()
        miconexion.close()
        micursor.close()

    except:
        talk(error)
    


def run():
    rec = listen('Esperando ordenes...')

    if 'crea la base de datos' in rec:
        name = rec.replace('crea la base de datos','')
        name = name.strip()
        command = editDataBase(name, True)
    
    elif 'edita la base de datos' in rec:
        order = rec.replace('edita la base de datos','')
        dataname = order.strip()

        talk('Que desea editar en la base de datos '+dataname+'?')
        rec = listen('Esperando ordenes...')

        if 'crear la tabla' in rec:
            order = rec.replace('crear la tabla','')
            tablename = order.strip()
            command = editTable(dataname, tablename, True)
        
        elif 'editar la tabla' in rec:
            tablename = rec.replace('editar la tabla','')
            tablename = tablename.strip()
            command = EditColumn(dataname, tablename)
        
        elif 'insertar datos en la tabla' in rec:
            tablename = rec.replace('insertar datos en la tabla','')
            tablename = tablename.strip()
            command = InsertData(dataname, tablename)
        
        elif 'eliminar la tabla' in rec:
            tablename = rec.replace('eliminar la tabla','')
            tablename = tablename.strip()
            command = editTable(dataname, tablename, False)

    
    elif 'borra la base de datos' in rec:
        name = rec.replace('borra la base de datos','')
        name = name.strip()
        command = editDataBase(name, False)

if __name__ == "__main__":
    run()





































