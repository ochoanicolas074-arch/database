import mssql_python
import json
from dotenv import load_dotenv
import os
class ConexionSqlServer:
    def __init__(self):
        load_dotenv()
        self.__server = os.getenv('THINKPAD-NICO')
        self.__database_name = os.getenv('northwind')
        self.__user = os.getenv('sa')
        self.__password = os.getenv('123456')
        self.__cnx = None
        self.__cursor = None
    def consulta(self,sql,parametros=None):
        try:
            if self.__cursor is None:
                if self.crear_conexion() is None:
                    return json.dumps({
                       'estado':False,
                       'mensaje':'No fue posible establecer la conexion'
                   },
                   ensure_ascii = False
                   )
            if parametros:
                self.__cursor.execute(sql,parametros)
            else:
                self.__cursor.execute(sql) 
                tipo = sql.split()[0].strip().upper()
                if tipo == 'SELECT':
                    columnas = []
                    for columna in self.__cursor.description:
                        columnas.append(columna[0])
                    registros = self.__cursor.fetchall()
                    resultados = []
                    for registro in registros:
                        fila = {}
                        for i,valor in enumerate(registro):
                            if type(valor) != 'Decimal': 
                                fila[columnas[i]] = f"{valor}"
                            else:
                                fila[columnas[i]] = valor

                        resultados.append(fila)
                    return json.dumps({
                        'estado':True,
                        'tipo':'select',
                        'registros': resultados
                    })
                elif tipo == "INSERT":
                    filas = self.__cursor.rowcount # Obtine el numero de rgistros afectados
                    self.__cnx.commit() # Comete la transacción
                    return json.dumps(
                        {
                            "estado": True,
                            "tipo": "INSERT",
                            "mensaje": "Registro insertado correctamente",
                            "filas_afectadas": filas
                        },
                        ensure_ascii=False
                    )
            # UPDATE
                elif tipo == "UPDATE":
                    filas = self.__cursor.rowcount
                    self.__cnx.commit()
                    return json.dumps(
                        {
                            "estado": True,
                            "tipo": "UPDATE",
                            "mensaje": "Registro actualizado correctamente",
                            "filas_afectadas": filas
                        },
                        ensure_ascii=False
                    )
            # DELETE
                elif tipo == "DELETE":
                    filas = self.__cursor.rowcount
                    self.__cnx.commit()
                    return json.dumps(
                        {
                            "estado": True,
                            "tipo": "DELETE",
                            "mensaje": "Registro eliminado correctamente",
                            "filas_afectadas": filas
                        },
                        ensure_ascii=False
                    )
            # OTRAS OPERACIONES
                else:
                    filas = self.cursor.rowcount
                    self.__cnx.commit()
                    return json.dumps(
                        {
                            "estado": True,
                            "tipo": tipo,
                            "mensaje": "Consulta ejecutada correctamente",
                            "filas_afectadas": filas
                        },
                        ensure_ascii=False
                    )
            # ERROR DE INTEGRIDAD
        except mssql_python.IntegrityError as e:
            if self.__cnx:
                    self.__cnx.rollback()
            return json.dumps(
                {
                    "estado": False,
                    "tipo": "IntegrityError",
                    "mensaje": "Violación de integridad en la base de datos",
                    "error": str(e)
                },
                ensure_ascii=False
            )
        # ERROR DE PROGRAMACIÓN SQL
        except mssql_python.ProgrammingError as e:
            if self.__cnx:
                self.__cnx.rollback()
            return json.dumps(
                {
                    "estado": False,
                    "tipo": "ProgrammingError",
                    "mensaje": "Error en la consulta SQL",
                    "error": str(e)
                },
                ensure_ascii=False
            )
        # ERROR GENERAL
        except mssql_python.Error as e:
            if self.__cnx:
                self.__cnx.rollback()
            return json.dumps(
                {
                    "estado": False,
                    "tipo": "DatabaseError",
                    "mensaje": "Error en la base de datos",
                    "error": str(e)
                },
                ensure_ascii=False
            )
        # ERROR DE PYTHON
        except Exception as e:
            if self.__cnx:
                self.__cnx.rollback()
            return json.dumps(
                {
                    "estado": False,
                    "tipo": "Error",
                    "mensaje": "Error inesperado",
                    "error": str(e)
                },
                ensure_ascii=False
            )
   
        except mssql_python.Error as e:
            print("Error al ejecutar la consulta en la base de datos")
            print(e)
                   
                
    def crear_conexion(self):
        try:
            cadena_con = (
                f"Server={self.__server},1433;"
                f"Database={self.__database_name};"
                f"UID={self.__user};"
                f"PWD={self.__password};"
                "Encrypt=yes;"
                "TrustServerCertificate=yes;"
            )
            self.__cnx = mssql_python.connect(cadena_con)
            self.__cursor = self.__cnx.cursor()
            print(f"Conectado al servidor {self.__server}")
        except mssql_python.Error as e:
            print(f"Error al conectarse al servidor {self.__server} de base de datos")
            print(e)
            self.__cnx = None
            self.__cursor = None
        return self.__cnx
    
    def cerrar_conexion(self):
        ban = False
        try:
            if self.__cursor:
                 self.__cursor.close()
                 self.__cursor = None
            if self.__cnx:
                self.__cnx = None
            ban = True
            print("se ha cerrado la conexion")
        except mssql_python.Error as e:
            print("Error al desconectarse de la base de datos")
            print(e)
        return ban


if __name__ == '__main__':
    cnn = ConexionSqlServer()
    cnn.crear_conexion()
    sql.select = """
                SELECT * FROM Customers
                """
    result = cnn.ejecutar_consulta(sql_select)
    cnn.cerrar_conexion()
    #Convertirel resultado en json
    result = json.loads(result)
    for r in result["registros"]:
        print(r)

        
    # Impresion de 1 en 1
    print(result)
    # resultado = json.loads(result["registros"])


    """
    sql1 = "select * from Products"
    sql2 = "DELETE Categories WHERE CategoryID=5"
    sql3 = "UPDATE Products SET UnitPrice = UnitPrice * 1.20 WHERE ProductID = 30"
    sql4 = "este-es-un-mensaje-para-separar/por-cadenas"
    a = sql1.split()[0]
    print(a)
    """