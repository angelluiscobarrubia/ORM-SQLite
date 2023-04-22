import sqlite3

class SQLite():

    def __init__(self,dirBDsqlite) -> None:
        self.DIRBD=dirBDsqlite+'.db'
    
    def crearBD(self):
        con=sqlite3.connect(self.DIRBD)
        con.commit()
        con.close()
        
    def execute(self,script):
        '''
        Metodo utilizado para:
        1-Crear Tablas
        2-Adicionar un elemento
        3-Modificar un elemento
        3-Eliminar un elemento
        '''
        con=sqlite3.connect(self.DIRBD)
        var_cursor=con.cursor()
        try:
            var_cursor.execute(script)
            con.commit()
            return var_cursor.lastrowid
        except Exception as exc:
            return self.MyException(exc)
        
    def crearTabla(self,script="TABLA(COL1, COL2)"):
        '''
        ---Crea una tabla---
        1-script: script de la tabla
        '''
        con=sqlite3.connect(self.DIRBD)        
        try:
        #--Buscando la tabla en la BD--
        #for x in var_cursor.execute("SELECT name FROM sqlite_master"):
        #    temptabla=x[0]
        #    if temptabla==name_tabla:
        #        return "La tabla ya esxiste"
            scriptfull="CREATE TABLE IF NOT EXISTS "+script  
            var_cursor=con.cursor()
            var_cursor.execute(scriptfull)
            con.commit()
            con.close()
            return True
        except Exception as exc:
            return False
            
    def insertarElemento(self,tabla='TABLA',*valores):
        '''
        Inserta un elemento en una tabla
        tabla: nombre de la Tabla
        valores: valores de los campos
        '''
        con=sqlite3.connect(self.DIRBD)
        try:
            cursor=con.cursor()
            script=f'INSERT INTO {tabla} values {valores}'
            cursor.execute(script)
            con.commit()
            con.close
            return True
        except Exception as exc:
            return False
    
    def insertarElementoDict(self,tabla='TABLA',valores = {'columna':'valor'}):
        '''
        Inserta un elemento en una tabla
        tabla: nombre de la Tabla
        valores: valores de los campos
        '''
        con=sqlite3.connect(self.DIRBD)
        try:
            cursor=con.cursor()
            columnas = ""
            value = ""
            for key,val in valores.items():
                columnas += key+','
                if isinstance(val, str):
                    value += f'"{val}",'
                else:
                    value += f'{val},'
            script=f'INSERT INTO {tabla}({columnas[:-1]}) values ({value[:-1]})'
            cursor.execute(script)
            con.commit()
            con.close
            return True
        except Exception as exc:
            return False
    
    def insertarElementos(self,tabla='TABLA',valores=[('val1'),('val2')]):
        '''
        Inserta varios elementos en una tabla
        tabla: nombre de la Tabla
        valores: lista de valores de los campos
        '''
        con=sqlite3.connect(self.DIRBD)
        try:
            #--Obteniendo la cantidad de valores por elemento
            cant_elementos=len(valores[0])
            script_values='('
            for ele in range(cant_elementos):
                if ele == (cant_elementos-1):
                    script_values=script_values+"?)"
                else:
                    script_values=script_values+"?,"
            #-------------------------------------------------
            cursor=con.cursor()
            script=f'INSERT INTO {tabla} values {script_values}'
            cursor.executemany(script,valores)
            con.commit()
            con.close
            return True
        except Exception as exc:
            return False
            
    def updateElemento(self,tabla,colCond,valCond,**valores):
        '''
        Modifica los valores de una fila
        tabla: nombre de la tabla
        colCond: Columna de la condicion
        valCond: Valor de la columna del elemento que queremos modificar
        valores: Diccionario con las columnas y valores que vamos a modificar
        '''
        con=sqlite3.connect(self.DIRBD)
        try:
            cursor=con.cursor()    
            #--Contruyendo el sql ---------------------------                      
            script=f'UPDATE {tabla} SET '# WHERE {campo}='
            for key,val in valores.items():               
                if isinstance(val,str):
                    script+=f'{key}="{val}",'
                else:
                    script+=f'{key}={val},'
            else: 
                script=script[:-1]       
                if isinstance(valCond,str):
                    script+=f' WHERE {colCond}="{valCond}"'
                else:
                    script+=f') WHERE {colCond}={valCond}'
            #-------------------------------------------------           
            cursor.execute(script)
            con.commit()
            con.close
            return True
        except Exception as exc:
            return False
        
    def eliminarElemento(self,tabla='TABLA',campo='COLUMNA',valor='0'):
        '''
        Elimina un elemento en una tabla
        tabla: nombre de la Tabla
        campo: campo para comparar
        valor: valor que vamos a buscar y eliminar 
        '''
        con=sqlite3.connect(self.DIRBD)
        try:
            cursor=con.cursor()                           
            script=f'DELETE FROM {tabla} WHERE {campo}='
            if isinstance(valor,int):
                script=script+str(valor)
            else:
                script=script+f'"{valor}"' 
            cursor.execute(script)
            con.commit()
            con.close
            return True
        except Exception as exc:
            return False
            
    def getFilasTabla(self,tabla='TABLA'):
        '''
        Devuelve una lista con todos los elementos
        tabla: nomnre de la tabla
        '''
        con=sqlite3.connect(self.DIRBD)
        try:
            var_cursor=con.cursor()
            script=f'SELECT * FROM {tabla}'
            datos=var_cursor.execute(script)
            result= datos.fetchall()
            return result
        except Exception as exc:
            return []   
          
    def sqlGetOne(self,sql):
        '''Devuelve el primer elemento de la consulta ejecutada.'''  
        con=sqlite3.connect(self.DIRBD)
        var_cursor=con.cursor()
        datos=var_cursor.execute(sql)
        result= datos.fetchone()
        return result[0]
      
    def sqlGetMany(self,sql):
        '''Devuelve todos los elementos del sql'''
        con=sqlite3.connect(self.DIRBD)
        var_cursor=con.cursor()
        datos=var_cursor.execute(sql)
        result= datos.fetchall()
        return result
    
    def MyException(self,exception):
        '''Metodo para procesar las excepciones'''
        pass

