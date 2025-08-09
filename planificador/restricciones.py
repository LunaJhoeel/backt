from typing import Set, Tuple, TYPE_CHECKING

from planificador.constantes import TURNOS

if TYPE_CHECKING:
    from planificador.estado import EstadoPlan

Dia = str
Turno = str
Enfermera = str


def respeta_max_consecutivos(estado: "EstadoPlan", enfermera: Enfermera, dia: Dia) -> bool:
    """
    Verifica que asignar (enfermera, dia) no rompa el limite de dias consecutivos
    """
    indice_actual: int = estado.indice_por_dia[dia]

    indices: Set[int] = {
        estado.indice_por_dia[d]
        for d in estado.dias_trabajados_por_enfermera[enfermera]
        if d in estado.indice_por_dia
    }

    izquierda: int = indice_actual
    while (izquierda - 1) in indices:
        izquierda -= 1

    derecha: int = indice_actual
    while (derecha + 1) in indices:
        derecha += 1

    racha: int = derecha - izquierda + 1
    return racha <= estado.max_dias_consecutivos


def es_candidata(estado: "EstadoPlan", enfermera: Enfermera, dia: Dia, turno: Turno) -> bool:
    """
    Verifica disponibilidad y reglas para (enfermera, dia, turno)
    """
    # Horarios declarados que les convienen a las licenciadas
    if turno not in estado.dominio_disponibilidad[(enfermera, dia)]:
        return False
    
    # Maximo un turno por persona y por dia
    if enfermera in estado.asignadas_por_dia[dia]:
        return False

    # Maximo turnos por semana
    if estado.total_turnos_por_enfermera[enfermera] >= estado.max_turnos_semana:
        return False

    # Maximo noches por semana
    if turno == "N" and estado.noches_por_enfermera[enfermera] >= estado.max_noches_semana:
        return False

    # Si trabajo noche anterior, no puede tomar siguiente manana
    indice_actual: int = estado.indice_por_dia[dia]
    if indice_actual > 0 and turno == "M":
        dia_anterior: Dia = estado.dias[indice_actual - 1]
        if enfermera in estado.plan[dia_anterior]["N"]:
            return False

    # Maximos dias consecutivos
    if not respeta_max_consecutivos(estado, enfermera, dia):
        return False

    return True
