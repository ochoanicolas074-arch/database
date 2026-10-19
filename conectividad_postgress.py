import psycopg2
import json


class ConectividadPostgres:

    def __init__(self):
        self.server = "localhost"
        self.port = 5432
        self.database_name = "northwindgpa"
        self.user = "postgres"
        self.password = "123456"

        self.cnx = None
        self.cursor = None

    # Método para crear la conexión
    def crear_conexion(self):
        try:
            self.cnx = psycopg2.connect(
                host=self.server,
                port=self.port,
                dbname=self.database_name,
                user=self.user,
                password=self.password
            )

            self.cursor = self.cnx.cursor()

            print(f"Conectado al servidor {self.server}")

            return self.cnx

        except psycopg2.Error as e:
            print(f"Error al conectarse al servidor {self.server}")
            print(e)

            self.cnx = None
            self.cursor = None

            return None

    # Método para ejecutar consultas SQL
    def ejecutar_consulta(self, sql, parametros=None):
        try:

            # Verificar conexión
            if self.cnx is None:

                if self.crear_conexion() is None:
                    return json.dumps(
                        {
                            "estado": False,
                            "mensaje": "No fue posible establecer la conexión"
                        },
                        ensure_ascii=False
                    )

            # Ejecutar consulta
            if parametros:
                self.cursor.execute(sql, parametros)
            else:
                self.cursor.execute(sql)

            # Identificar el tipo de consulta
            tipo = sql.strip().split()[0].upper()

            # SELECT
            if tipo == "SELECT":

                columnas = []

                for columna in self.cursor.description:
                    columnas.append(columna[0])

                registros = self.cursor.fetchall()

                resultado = []

                for registro in registros:

                    fila = {}

                    for i, valor in enumerate(registro):
                        fila[columnas[i]] = valor

                    resultado.append(fila)

                return json.dumps(
                    {
                        "estado": True,
                        "tipo": "SELECT",
                        "registros": resultado
                    },
                    default=str,
                    ensure_ascii=False
                )

            # INSERT
            elif tipo == "INSERT":

                filas = self.cursor.rowcount

                self.cnx.commit()

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

                filas = self.cursor.rowcount

                self.cnx.commit()

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

                filas = self.cursor.rowcount

                self.cnx.commit()

                return json.dumps(
                    {
                        "estado": True,
                        "tipo": "DELETE",
                        "mensaje": "Registro eliminado correctamente",
                        "filas_afectadas": filas
                    },
                    ensure_ascii=False
                )

            # OTRAS CONSULTAS
            else:

                filas = self.cursor.rowcount

                self.cnx.commit()

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
        except psycopg2.IntegrityError as e:

            if self.cnx:
                self.cnx.rollback()

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
        except psycopg2.ProgrammingError as e:

            if self.cnx:
                self.cnx.rollback()

            return json.dumps(
                {
                    "estado": False,
                    "tipo": "ProgrammingError",
                    "mensaje": "Error en la consulta SQL",
                    "error": str(e)
                },
                ensure_ascii=False
            )

        # ERROR GENERAL DE BASE DE DATOS
        except psycopg2.Error as e:

            if self.cnx:
                self.cnx.rollback()

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

            if self.cnx:
                self.cnx.rollback()

            return json.dumps(
                {
                    "estado": False,
                    "tipo": "Error",
                    "mensaje": "Error inesperado",
                    "error": str(e)
                },
                ensure_ascii=False
            )

    # Método para cerrar la conexión
    def cerrar_conexion(self):
        try:

            if self.cursor:
                self.cursor.close()
                self.cursor = None

            if self.cnx:
                self.cnx.close()
                self.cnx = None

            print(
                f"Se ha cerrado la conexión "
                f"con el servidor {self.server}"
            )

            return True

        except psycopg2.Error as e:

            print(
                "Error al desconectarse "
                "del servidor de base de datos"
            )

            print(e)

            return False


# Programa principal
def main():

    cnn = ConectividadPostgres()

    # 1. Crear conexión
    print("--- 1. CREAR CONEXIÓN ---")

    if cnn.crear_conexion() is None:
        return

    # 2. SELECT
    print("--- 2. SELECT ---")

    print(
        cnn.ejecutar_consulta(
            "SELECT categoryid, categoryname FROM categories"
        )
    )

    # 3. UPDATE
    print("--- 3. UPDATE ---")

    print(
        cnn.ejecutar_consulta(
            "UPDATE products "
            "SET unitsinstock = unitsinstock + 1 "
            "WHERE productid = %s",
            (78,)
        )
    )

    # 4. DELETE
    print("--- 4. DELETE ---")

    print(
        cnn.ejecutar_consulta(
            "DELETE FROM categories "
            "WHERE categoryid = %s",
            (5,)
        )
    )

    # 5. Consulta solicitada por el profesor
    print("--- 5. CONSULTA CON JOIN ---")

    sql = """
        SELECT
            C.company_name,
            O.order_id,
            P.product_name,
            OD.quantity,
            OD.unit_price,
            OD.discount,
            (
                (OD.quantity * OD.unit_price)
                -
                (OD.quantity * OD.unit_price * OD.discount)
            ) AS subtotal
        FROM customers C
        INNER JOIN orders O
            ON C.customer_id = O.customer_id
        INNER JOIN order_details OD
            ON O.order_id = OD.order_id
        INNER JOIN products P
            ON OD.product_id = P.product_id
        WHERE O.order_id = %(order_id)s;
    """

    parametros = {
        "order_id": 10248
    }

    resultado = cnn.ejecutar_consulta(sql, parametros)

    print(resultado)

    # 6. Cerrar conexión
    print("--- 6. CERRAR CONEXIÓN ---")

    print(cnn.cerrar_conexion())


if __name__ == '__main__':
    main()