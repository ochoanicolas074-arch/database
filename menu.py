
import json
from conexion_coffe import ConexionCoffe


class Menu:

    def __init__(self):
        self.conexion = ConexionCoffe()

    def mostrar_menu(self):
        while True:
            print("\n" + "=" * 38)
            print("       SISTEMA DE CAFETERÍA COFFE")
            print("=" * 38)
            print("1. Crear categoría")
            print("2. Consultar categorías")
            print("3. Actualizar categoría")
            print("4. Eliminar categoría")
            print("5. Salir")
            print("=" * 38)

            opcion = input("Selecciona una opción: ").strip()

            if opcion == "1":
                self.crear()
            elif opcion == "2":
                self.consultar()
            elif opcion == "3":
                self.actualizar()
            elif opcion == "4":
                self.eliminar()
            elif opcion == "5":
                self.conexion.cerrar_conexion()
                print("¡Gracias por utilizar COFFE!")
                break
            else:
                print("Opción no válida. Intenta nuevamente.")

    def ejecutar(self, sql, parametros=None):
        resultado = self.conexion.ejecutar_consulta(
            sql, parametros
        )
        return json.loads(resultado)

    def crear(self):
        print("\n--- CREAR CATEGORÍA ---")

        nombre = input("Nombre de la categoría: ").strip()
        descripcion = input("Descripción: ").strip()

        if not nombre:
            print("El nombre es obligatorio.")
            return

        resultado = self.ejecutar(
            """
            INSERT INTO public."Categorias"
                ("Nombre", "Descripcion")
            VALUES (%s, %s)
            """,
            (nombre, descripcion or None)
        )

        if resultado.get("estado"):
            print("Categoría creada correctamente.")
        else:
            print("No se pudo crear la categoría.")
            print(resultado.get("error", resultado.get("mensaje")))

    def consultar(self):
        print("\n--- CONSULTAR CATEGORÍAS ---")

        resultado = self.ejecutar(
            """
            SELECT "Id_Categoria", "Nombre",
                   "Descripcion", "Estado"
            FROM public."Categorias"
            ORDER BY "Id_Categoria"
            """
        )

        if not resultado.get("estado"):
            print("Error:", resultado.get("error",
                                          resultado.get("mensaje")))
            return

        registros = resultado.get("registros", [])

        if not registros:
            print("No hay categorías registradas.")
            return

        print("-" * 75)
        print(f"{'ID':<6} {'NOMBRE':<22} {'DESCRIPCIÓN':<32} {'ESTADO'}")
        print("-" * 75)

        for categoria in registros:
            estado = (
                "Activo" if categoria["Estado"] else "Inactivo"
            )
            descripcion = categoria["Descripcion"] or ""

            print(
                f'{categoria["Id_Categoria"]:<6} '
                f'{categoria["Nombre"][:21]:<22} '
                f'{descripcion[:31]:<32} '
                f'{estado}'
            )

        print("-" * 75)

    def actualizar(self):
        print("\n--- ACTUALIZAR CATEGORÍA ---")

        try:
            id_categoria = int(
                input("ID de la categoría que deseas actualizar: ")
            )
        except ValueError:
            print("Debes ingresar un ID numérico.")
            return

        nombre = input("Nuevo nombre: ").strip()
        descripcion = input("Nueva descripción: ").strip()

        if not nombre:
            print("El nombre es obligatorio.")
            return

        resultado = self.ejecutar(
            """
            UPDATE public."Categorias"
            SET "Nombre" = %s,
                "Descripcion" = %s
            WHERE "Id_Categoria" = %s
            """,
            (nombre, descripcion or None, id_categoria)
        )

        if not resultado.get("estado"):
            print("Error:", resultado.get("error",
                                          resultado.get("mensaje")))
        elif resultado.get("filas_afectadas", 0) > 0:
            print("Categoría actualizada correctamente.")
        else:
            print("No se encontró una categoría con ese ID.")

    def eliminar(self):
        print("\n--- ELIMINAR CATEGORÍA ---")

        try:
            id_categoria = int(
                input("ID de la categoría que deseas eliminar: ")
            )
        except ValueError:
            print("Debes ingresar un ID numérico.")
            return

        confirmar = input(
            f"¿Seguro que deseas eliminar la categoría "
            f"{id_categoria}? (s/n): "
        ).strip().lower()

        if confirmar != "s":
            print("Operación cancelada.")
            return

        resultado = self.ejecutar(
            """
            DELETE FROM public."Categorias"
            WHERE "Id_Categoria" = %s
            """,
            (id_categoria,)
        )

        if not resultado.get("estado"):
            print(
                "No se pudo eliminar. Puede que la categoría "
                "esté relacionada con productos."
            )
            print(resultado.get("error", resultado.get("mensaje")))
        elif resultado.get("filas_afectadas", 0) > 0:
            print("Categoría eliminada correctamente.")
        else:
            print("No se encontró una categoría con ese ID.")
