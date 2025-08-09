import time
from collections import defaultdict

turnos = ["M", "T", "N"]  # Manhana, Tarde, Noche

def planificar_turnos_enfermeros(
    dias,
    enfermeros,
    cobertura,
    disponibilidad,
    max_turnos_semana = 5,
    max_noches_semana = 2,
    max_dias_consecutivos = 4,
):
    plan = {}
    for dia in dias:
        plan[dia] = {}
        for turno in turnos:
            plan[dia][turno] = []

    asignadas_por_dia = {}
    for dia in dias:
        asignadas_por_dia[dia] = set()

    total_turnos_por_enfermera = defaultdict(int)
    noches_por_enfermera = defaultdict(int)
    dias_trabajados_por_enfermera = defaultdict(set)

    indice_por_dia = {}
    for i, dia in enumerate(dias):
        indice_por_dia[dia] = i

    dominio_disponibilidad = {}
    for enfermera in enfermeros:
        for dia in dias:
            dominio_disponibilidad[(enfermera, dia)] = set()
            if enfermera in disponibilidad:
                for turno in turnos:
                    if (dia, turno) in disponibilidad[enfermera]:
                        dominio_disponibilidad[(enfermera, dia)].add(turno)

    contador_recursiones = 0
    contador_retrocesos = 0

    def seleccionar_siguiente_dia_turno():
        mejor_dia_turno = None
        minimo_candidatas = float("inf")

        for dia in dias:
            for turno in turnos:
                cupos_pendientes = cobertura[dia][turno] - len(plan[dia][turno])
                if cupos_pendientes <= 0:
                    continue

                candidatas_posibles = []
                for enfermera in enfermeros:
                    if es_enfermera_candidata(enfermera, dia, turno):
                        candidatas_posibles.append(enfermera)

                if len(candidatas_posibles) == 0:
                    return (dia, turno)

                if len(candidatas_posibles) < minimo_candidatas:
                    mejor_dia_turno = (dia, turno)
                    minimo_candidatas = len(candidatas_posibles)

        return mejor_dia_turno

    def es_enfermera_candidata(enfermera, dia, turno):
        if turno not in dominio_disponibilidad[(enfermera, dia)]:
            return False

        if enfermera in asignadas_por_dia[dia]:
            return False

        if total_turnos_por_enfermera[enfermera] >= max_turnos_semana:
            return False

        if turno == "N" and noches_por_enfermera[enfermera] >= max_noches_semana:
            return False

        indice_actual = indice_por_dia[dia]
        if indice_actual > 0 and turno == "M":
            dia_anterior = dias[indice_actual - 1]
            if enfermera in plan[dia_anterior]["N"]:
                return False

        if not respeta_max_consecutivos(enfermera, dia):
            return False

        return True

    def respeta_max_consecutivos(enfermera, dia):
        indice_actual = indice_por_dia[dia]
        indices = set()

        for dia_trabajado in dias_trabajados_por_enfermera[enfermera]:
            idx = indice_por_dia.get(dia_trabajado)
            if idx is not None:
                indices.add(idx)

        izquierda = indice_actual
        while (izquierda - 1) in indices:
            izquierda -= 1

        derecha = indice_actual
        while (derecha + 1) in indices:
            derecha += 1

        racha = derecha - izquierda + 1
        return racha <= max_dias_consecutivos

    def asignar_enfermera(enfermera, dia, turno):
        plan[dia][turno].append(enfermera)
        asignadas_por_dia[dia].add(enfermera)
        total_turnos_por_enfermera[enfermera] += 1

        if turno == "N":
            noches_por_enfermera[enfermera] += 1

        dias_trabajados_por_enfermera[enfermera].add(dia)
        print(f"Asignar: {enfermera} -> {dia} {turno}")

    def desasignar_enfermera(enfermera, dia, turno):
        if enfermera in plan[dia][turno]:
            plan[dia][turno].remove(enfermera)

        if enfermera in asignadas_por_dia[dia]:
            asignadas_por_dia[dia].remove(enfermera)

        total_turnos_por_enfermera[enfermera] -= 1

        if turno == "N":
            noches_por_enfermera[enfermera] -= 1

        if dia in dias_trabajados_por_enfermera[enfermera]:
            dias_trabajados_por_enfermera[enfermera].remove(dia)

        print(f"Retroceder: {enfermera} <- {dia} {turno}")

    def clave_orden_candidatas(enfermera):
        return (total_turnos_por_enfermera[enfermera], noches_por_enfermera[enfermera])

    def resolver_backtracking():
        nonlocal contador_recursiones, contador_retrocesos
        contador_recursiones += 1

        siguiente = seleccionar_siguiente_dia_turno()
        if siguiente is None:
            return True

        dia_actual, turno_actual = siguiente

        candidatas_posibles = []
        for enfermera in enfermeros:
            if es_enfermera_candidata(enfermera, dia_actual, turno_actual):
                candidatas_posibles.append(enfermera)

        candidatas_posibles.sort(key = clave_orden_candidatas)

        for enfermera in candidatas_posibles:
            asignar_enfermera(enfermera, dia_actual, turno_actual)
            if resolver_backtracking():
                return True
            # Fallo la rama: retroceso
            contador_retrocesos += 1
            desasignar_enfermera(enfermera, dia_actual, turno_actual)

        return False

    solucion_encontrada = resolver_backtracking()
    if solucion_encontrada:
        return plan, contador_recursiones, contador_retrocesos
    else:
        return None, contador_recursiones, contador_retrocesos


if __name__ == "__main__":
    dias = ["Lun", "Mar", "Mie", "Jue", "Vie"]
    enfermeros = ["Ana", "Luis", "Marta", "Cris", "Eva"]

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
        "Luis": {
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

    inicio = time.time()
    plan, recursiones, retrocesos = planificar_turnos_enfermeros(
        dias, enfermeros, cobertura, disponibilidad,
        # POliticas del hospital
        max_turnos_semana = 5,
        max_noches_semana = 2,
        max_dias_consecutivos = 4,
    )
    fin = time.time()

    if plan is None:
        print("No hay solucion con las restricciones dadas.")
    else:
        print("\nPlan encontrado:")
        for dia in dias:
            print(f"\n{dia}:")
            for turno in turnos:
                asignadas = ""
                indice = 0
                for enfermera in plan[dia][turno]:
                    if indice == 0:
                        asignadas = enfermera
                    else:
                        asignadas = asignadas + ", " + enfermera
                    indice += 1
                print(f"  {turno}: {asignadas}")

    duracion = fin - inicio
    print(f"\nTiempo total de ejecucion (planificacion): {duracion:.6f} s")
    print(f"Recursiones totales: {recursiones}")
    print(f"Retrocesos totales: {retrocesos}")
