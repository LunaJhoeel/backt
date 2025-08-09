import time
from planificador import TURNOS, EstadoPlan, SolverBacktracking

def imprimir_plan(dias, plan):
    """
    Imprime el plan por dia y por turno
    """
    i = 0
    while i < len(dias):
        d = dias[i]
        print("\n" + str(d) + ":")
        j = 0
        while j < len(TURNOS):
            t = TURNOS[j]
            asignadas = ""
            k = 0
            while k < len(plan[d][t]):
                nombre = plan[d][t][k]
                if k == 0:
                    asignadas = nombre
                else:
                    asignadas = asignadas + ", " + nombre
                k += 1
            print("  " + str(t) + ": " + asignadas)
            j += 1
        i += 1

if __name__ == "__main__":
    dias = ["Lun", "Mar", "Mie", "Jue", "Vie"]
    enfermeros = ["Ana", "Luisa", "Marta", "Cris", "Eva"]

    # Se necesitan 2 enfermeros en las manhanas por mayor demanda de atenciones
    cobertura = {
        "Lun": {"M": 2, "T": 1, "N": 1},  # 2 en Manhana, 1 en Tarde, 1 en Noche
        "Mar": {"M": 2, "T": 1, "N": 1},
        "Mie": {"M": 2, "T": 1, "N": 1},
        "Jue": {"M": 2, "T": 1, "N": 1},
        "Vie": {"M": 2, "T": 1, "N": 1}
    }

    # Los licenciados en enfermerian han determinado los horarios que les convienen
    disponibilidad = {
        "Ana": {
            ("Lun", "M"),
            ("Lun", "N"),
            ("Lun", "T"),
            ("Mar", "M"),
            ("Mar", "T"),
            ("Mie", "M"),
            ("Mie", "T"),
            ("Jue", "M"),
            ("Jue", "T"),
            ("Vie", "M"),
            ("Vie", "T")
        },
        "Luisa": {
            ("Lun", "M"),
            ("Lun", "T"),
            ("Lun", "N"),
            ("Mar", "M"),
            ("Mar", "T"),
            ("Mar", "N"),
            ("Mie", "M"),
            ("Mie", "T"),
            ("Mie", "N"),
            ("Jue", "M"),
            ("Jue", "T"),
            ("Jue", "N"),
            ("Vie", "M"),
            ("Vie", "T"),
            ("Vie", "N")
        },
        "Marta": {
            ("Lun", "M"),
            ("Lun", "N"),
            ("Mar", "M"),
            ("Mar", "N"),
            ("Mie", "M"),
            ("Mie", "T"),
            ("Mie", "N"),
            ("Jue", "M"),
            ("Jue", "T"),
            ("Jue", "N"),
            ("Vie", "M"),
            ("Vie", "N")
        },
        "Cris": {
            ("Lun", "T"),
            ("Lun", "N"),
            ("Mar", "T"),
            ("Mar", "N"),
            ("Mie", "T"),
            ("Mie", "N"),
            ("Jue", "T"),
            ("Jue", "N"),
            ("Vie", "T"),
            ("Vie", "N")
        },
        "Eva": {
            ("Lun", "M"),
            ("Mar", "T"),
            ("Mie", "N"),
            ("Vie", "M")
        }
    }

    try:
        inicio = time.time()
        estado = EstadoPlan(
            dias=dias,
            enfermeros=enfermeros,
            cobertura=cobertura,
            disponibilidad=disponibilidad,
            max_turnos_semana=5,
            max_noches_semana=2,
            max_dias_consecutivos=4,
            verbose=True,
        )
        solver = SolverBacktracking(estado)
        exito = solver.resolver()
        fin = time.time()

        if not exito:
            print("No hay solucion con las restricciones dadas.")
        else:
            print("\nPlan encontrado:")
            imprimir_plan(dias, estado.plan)

        duracion = fin - inicio
        print("\nTiempo total de ejecucion (planificacion): " + "{:.6f}".format(duracion) + " s")
        print("Recursiones totales: " + str(estado.contador_recursiones))
        print("Retrocesos totales: " + str(estado.contador_retrocesos))

    except ValueError as e:
        print("Error de validacion de datos: " + str(e))
    except Exception as e:
        print("Error inesperado: " + str(e))
