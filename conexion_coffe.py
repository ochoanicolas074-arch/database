
import psycopg2
import json


class ConexionCoffe:

    def __init__(self):
        self.server = "localhost"
        self.port = 5432
        self.database_name = "COFFE"
        self.user = "postgres"
        self.password = "123456"  # Cambia esto por tu contraseña real

        self.cnx = None
        self.cursor = None

    # Crear conexión
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

            print("¡Conexión exitosa a PostgreSQL!")
            print(f"Base de datos: {self.database_name}")

            return self.cnx

        except psycopg2.Error as e:
            print("Error al conectarse a PostgreSQL:")
            print(e)

            self.cnx = None
            self.cursor = None

            return None

    # Ejecutar consultas SQL
    def ejecutar_consulta(self, sql, parametros=None):
        try:
            if self.cnx is None or self.cnx.closed:
                if self.crear_conexion() is None:
                    return json.dumps({
                        "estado": False,
                        "mensaje": "No fue posible establecer la conexión"
                    }, ensure_ascii=False)

            self.cursor.execute(sql, parametros)

            tipo = sql.strip().split()[0].upper()

            if tipo == "SELECT":
                columnas = [
                    columna[0]
                    for columna in self.cursor.description
                ]

                registros = self.cursor.fetchall()

                resultado = [
                    dict(zip(columnas, registro))
                    for registro in registros
                ]

                return json.dumps({
                    "estado": True,
                    "tipo": "SELECT",
                    "registros": resultado
                }, default=str, ensure_ascii=False)

            else:
                filas = self.cursor.rowcount
                self.cnx.commit()

                return json.dumps({
                    "estado": True,
                    "tipo": tipo,
                    "mensaje": "Consulta ejecutada correctamente",
                    "filas_afectadas": filas
                }, ensure_ascii=False)

        except psycopg2.Error as e:
            if self.cnx and not self.cnx.closed:
                self.cnx.rollback()

            return json.dumps({
                "estado": False,
                "mensaje": "Error en la consulta SQL",
                "error": str(e)
            }, ensure_ascii=False)

    # Cerrar conexión
    def cerrar_conexion(self):
        try:
            if self.cursor and not self.cursor.closed:
                self.cursor.close()

            self.cursor = None

            if self.cnx and not self.cnx.closed:
                self.cnx.close()

            self.cnx = None

            print("Conexión cerrada correctamente.")
            return True

        except psycopg2.Error as e:
            print("Error al cerrar la conexión:")
            print(e)
            return False


# Programa principal para probar la conexión
def main():
    cnn = ConexionCoffe()

    print("--- CONEXIÓN A COFFE ---")

    if cnn.crear_conexion() is None:
        return

    print("--- CONSULTAR CATEGORÍAS ---")

    resultado = cnn.ejecutar_consulta(
        'SELECT * FROM "Categorias"'
    )
    print(resultado)

    print("--- CERRAR CONEXIÓN ---")
    cnn.cerrar_conexion()


if __name__ == "__main__":
    main()