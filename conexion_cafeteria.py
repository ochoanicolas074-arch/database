import mssql_python

servidor = "THINKPAD-NICO,1433"
base_datos = "COFFE"
usuario = "sa"
contrasena = "123456"

cadena = (
    f"Server={servidor};"
    f"Database={base_datos};"
    f"UID={usuario};"
    f"PWD={contrasena};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

try:
    conexion = mssql_python.connect(cadena)
    cursor = conexion.cursor()

    cursor.execute("SELECT DB_NAME()")
    resultado = cursor.fetchone()

    print("¡Conexión exitosa!")
    print("Base de datos:", resultado[0])

    cursor.close()
    conexion.close()

except Exception as error:
    print("Error de conexión:", error)
