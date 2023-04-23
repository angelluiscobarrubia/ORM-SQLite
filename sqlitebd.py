import sqlite3

class SQLite():

    def __init__(self,dirBDsqlite) -> None:
        self.DIRBD=dirBDsqlite+'.db'
        self.fun_CrearBD()
    
    def fun_CrearBD(self):
        '''Crea la BD '''
        con=sqlite3.connect(self.DIRBD)
        con.commit()
        con.close()
        
    def fun_EjecutarScript(self,script):
        '''
        Metodo utilizado para:
        1-Crear Tablas
        2-Adicionar un elemento
        3-Modificar un elemento
        3-Eliminar un elemento

        script: script que se desea ejecutar
        '''
        con=sqlite3.connect(self.DIRBD)
        var_cursor=con.cursor()
        try:
            var_cursor.execute(script)
            con.commit()
            return True
        except Exception as exc:
            return False
        
    def fun_CrearTabla(self,script="TABLA(COL1, COL2)"):
        '''
        ---Crea una tabla---
        script: script de la tabla
        '''
        con=sqlite3.connect(self.DIRBD)        
        try:
            scriptfull="CREATE TABLE IF NOT EXISTS "+script  
            var_cursor=con.cursor()
            var_cursor.execute(scriptfull)
            con.commit()
            con.close()
            return True
        except Exception as exc:
            return False
            
    def fun_InsertarElemento(self,tabla='TABLA',*valores):
        '''
        Inserta un elemento en una tabla
        tabla: nombre de la Tabla
        valores: valores de los campos (deben coincidir con el orden de las columnas en la tabla)
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
    
    def fun_InsertarElementoDict(self,tabla='TABLA',valores = {'columna':'valor'}):
        '''
        Inserta un elemento en una tabla
        tabla: nombre de la Tabla
        valores: diccionario con los valores de las columnas que se van a adicionar 
        '''
        con=sqlite3.connect(self.DIRBD)
        try:
            cursor=con.cursor()
            #--Construyendo el script-----------------------------------------------
            columnas = ""
            value = ""
            for key,val in valores.items():
                columnas += key+','
                if isinstance(val, str):
                    value += f'"{val}",'
                else:
                    value += f'{val},'
            script=f'INSERT INTO {tabla}({columnas[:-1]}) values ({value[:-1]})'
            #-----------------------------------------------------------------------
            cursor.execute(script)
            con.commit()
            con.close
            return True
        except Exception as exc:
            return False
    
    def fun_InsertarElementos(self,tabla='TABLA',valores=[('val1'),('val2')]):
        '''
        Inserta varios elementos en una tabla
        tabla: nombre de la Tabla
        valores: lista de (tuplas) que contiene los valores de los campos
                 (deben coincidir con el orden de las columnas en la tabla).
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
            
    def fun_InsertarElementosDict(self,tabla='TABLA',valores=[{'col1':'val1'}]):
        '''
        Inserta varios elementos en una tabla
        tabla: nombre de la Tabla
        valores: lista de (diccionarios) que contiene los valores de los campos
        '''
        con=sqlite3.connect(self.DIRBD)
        try:            
            for valdic in valores:
                self.fun_InsertarElementoDict(tabla,valdic)
            return True
        except Exception as exc:
            return False

    def fun_ModificarElemento(self,tabla,colCond,valCond,**valores):
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
        
    def fun_EliminarElemento(self,tabla='TABLA',columna='COLUMNA',valor='0'):
        '''
        Elimina un elemento en una tabla
        tabla: nombre de la Tabla
        columna: nombre de la columna para comparar
        valor: valor de la columna que vamos a buscar para eliminar el elemento
        '''
        con=sqlite3.connect(self.DIRBD)
        try:
            cursor=con.cursor()                           
            script=f'DELETE FROM {tabla} WHERE {columna}='
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
            
    def fun_ObtenerTodaLaTabla(self,tabla='TABLA'):
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
            con.close()
            return result
        except Exception as exc:
            return []   
          
    def fun_ObtenerUnElemento(self,sql):
        '''
        Devuelve el primer elemento de la consulta ejecutada.
        sql: script que se va a ejecutar

        Nota: en caso de no encontrase un elemento devuelve (None).
        '''  
        con=sqlite3.connect(self.DIRBD)
        try:
            var_cursor=con.cursor()
            datos=var_cursor.execute(sql)
            result= datos.fetchone()
            con.close()
            return result[0]
        except Exception as exc:
            return None
      
    def fun_ObtenerMuchosElementos(self,sql):
        '''
        Devuelve varios elementos
        sql: script que se va a ejecutar
        
        Nota: en caso de no encontrase ningun elemento e dispararse 
        una (Exception) devuelve una tupla vacia ().
        '''
        con=sqlite3.connect(self.DIRBD)
        try:
            var_cursor=con.cursor()
            datos=var_cursor.execute(sql)
            result= datos.fetchall()
            con.close()
            return result
        except Exception as exc:
            return ()

    def MyException(self,exception):
        '''Metodo para procesar las excepciones'''
        pass

