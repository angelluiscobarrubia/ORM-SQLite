from sqlitebd import SQLite

#print()
#nameBD=input("Introduzca el nombe de la BD \n")
#print("Introduzca la carpeta de la BD")
#dirBD=input()

mybd=SQLite('bd1')
#tempcreate= mybd.crearTabla(script="novela(title, year, score)")
#print(f'{tempcreate}')
'''
mybd.M_CreateBD()
mybd.M_Execute("CREATE TABLE movie(title, year, score)")
print("Tabla creada")
'''
#val1=mybd.insertarElementos('NOVELA',[('novela1',2001,100),('novela2',2002,102),('novela3',2003,103)])
#print(val1)

novelas=mybd.getFilasTabla('novela')
print(novelas)

mybd.updateElemento('novela','title','novela1',year=1908, title='novela10', score=123)
#val2=mybd.eliminarElemento('NOVELA','score',102)
#onelemet=mybd.M_SQLGetMany("SELECT name FROM sqlite_master")
#print(f"Obteniendo tablas: {onelemet}")