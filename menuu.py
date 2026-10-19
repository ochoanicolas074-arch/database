import os
import json
from conectividad_postgress import ConectividadPostgres


# -------------------- UTILIDADES DE CONSOLA --------------------

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_table(rows, headers):

    if not rows:
        print("  (sin resultados)")
        return

    col_widths = {h: len(h) for h in headers}

    for r in rows:
        for h in headers:
            col_widths[h] = max(
                col_widths[h],
                len(str(r.get(h, '')))
            )

    line = "+" + "+".join(
        "-" * (col_widths[h] + 2)
        for h in headers
    ) + "+"

    print(line)

    header_row = "| " + " | ".join(
        str(h).ljust(col_widths[h])
        for h in headers
    ) + " |"

    print(header_row)
    print(line)

    for r in rows:

        row_str = "| " + " | ".join(
            str(r.get(h, '')).ljust(col_widths[h])
            for h in headers
        ) + " |"

        print(row_str)

    print(line)


# -------------------- CLASE MENU PRINCIPAL --------------------

class MenuNorthwind:

    def mostrar_banner(self):
        print("="*70)
        print("  ███╗   ██╗ ██████╗ ██████╗ ████████╗██╗  ██╗██╗    ██╗██╗███╗   ██╗██████╗ ".center(70))
        print("  ████╗  ██║██╔═══██╗██╔══██╗╚══██╔══╝██║  ██║██║    ██║██║████╗  ██║██╔══██╗".center(70))
        print("  ██╔██╗ ██║██║   ██║██████╔╝   ██║   ███████║██║ █╗ ██║██║██╔██╗ ██║██║  ██║".center(70))
        print("  ██║╚██╗██║██║   ██║██╔══██╗   ██║   ██╔══██║██║███╗██║██║██║╚██╗██║██║  ██║".center(70))
        print("  ██║ ╚████║╚██████╔╝██║  ██║   ██║   ██║  ██║╚███╔███╔╝██║██║ ╚████║██████╔╝".center(70))
        print("="*70)
        print("           GESTOR DE PEDIDOS - CONSOLA ".center(70))
        print("="*70)

    def mostrar_menu(self):

        print("""
        ┌─────────────────────────────────────────────────────┐
        │                   MENÚ PRINCIPAL                    │
        ├─────────────────────────────────────────────────────┤
        │  1) Ver últimos pedidos (INNER JOIN)                │
        │  2) Ver detalle de un pedido                        │
        │  3) Crear nuevo pedido                              │
        │  4) Eliminar pedido                                 │
        │  5) Buscar pedidos por cliente (LEFT JOIN)          │
        │  6) Clientes que nunca han pedido (LEFT JOIN+NULL)  │
        │  7) Productos nunca vendidos (LEFT JOIN+NULL)       │
        │  8) Estadísticas y TOP clientes                     │
        │  9) Ver 10 consultas de ejemplo (INNER/LEFT/RIGHT)  │
        │  0) Salir                                           │
        └─────────────────────────────────────────────────────┘
        """)


    def run(self):

        while True:

            clear()

            self.mostrar_banner()
            self.mostrar_menu()

            try:

                opc = input(
                    "  👉 Selecciona una opción [0-9]: "
                ).strip()

            except (KeyboardInterrupt, EOFError):

                print("\nSaliendo...")
                break


            if opc == "1":

                self.op_ver_pedidos()

            elif opc == "0":

                print("\n¡Hasta luego! 👋")
                break

            else:

                print("\n❌ Opción no válida")


            input("\nPresiona ENTER para continuar...")


    # -------------------- OPCIÓN 1 --------------------

    def op_ver_pedidos(self):

        clear()

        print(
            "\n📦 ÚLTIMOS 10 PEDIDOS "
            "(con INNER JOIN a customers)\n"
        )

        conn = None

        try:

            conn = ConectividadPostgres()

            sql = """
                select
                    o.order_id as "Num_Order",
                    c.company_name as "Empresa",
                    o.order_date as "Fecha",
                    o.ship_country as "Pais"
                from orders o
                inner join customers c
                    on o.customer_id = c.customer_id
                order by o.order_date desc
                limit %(limite)s
            """

            result = conn.ejecutar_consulta(
                sql,
                {"limite": 10}
            )

            if result is None:

                print("❌ No se obtuvieron resultados.")
                return

            # La clase devuelve JSON en texto
            if isinstance(result, str):

                result = json.loads(result)

            rows = result["registros"]

            print_table(
                rows,
                [
                    "Num_Order",
                    "Empresa",
                    "Fecha",
                    "Pais"
                ]
            )

        except Exception as e:

            print(f"❌ Error: {e}")

        finally:

            if conn is not None:

                conn.cerrar_conexion()


# -------------------- MAIN --------------------

if __name__ == "__main__":

    m = MenuNorthwind()
    m.run()