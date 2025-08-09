from typing import Optional, Tuple, TYPE_CHECKING

from planificador.constantes import TURNOS
from planificador.restricciones import es_candidata

if TYPE_CHECKING:
    from planificador.estado import EstadoPlan  # evita import circular

Dia = str
Turno = str
Enfermero = str


def seleccionar_siguiente_dia_turno(estado: "EstadoPlan") -> Optional[Tuple[Dia, Turno]]:
    """
    Heuristica MRV: elige (dia, turno) con cupos pendientes y menos candidatos
    Si algun (dia, turno) tiene 0 candidatas, se retorna de inmediato para forzar retroceso
    
    Parametros:
    estado : EstadoPlan
        Estado con plan parcial, cobertura, disponibilidad, contadores e indices.

    Retorna:
    Optional[Tuple[Dia, Turno]]
        - (dia, turno) con el menor numero de candidatas segun MRV
        - None si ya no quedan cupos pendientes (exito)
    """
    
    mejor: Optional[Tuple[Dia, Turno]] = None
    minimo: float = float("inf")

    for d in estado.dias:
        for t in TURNOS:
            cupos: int = estado.cobertura[d][t] - len(estado.plan[d][t])
            if cupos <= 0:
                continue
            
            # Cuenta cuantas candidatas tiene este dia y turno
            candidatas = [e for e in estado.enfermeros if es_candidata(estado, e, d, t)]
            
            # Fail-first: si no hay candidatas, devuelve este dia y turno de inmediato
            if len(candidatas) == 0:
                return (d, t)

            # Elige el (dia, turno) con la menor cantidad de candidatas
            if len(candidatas) < minimo:
                minimo = len(candidatas)
                mejor = (d, t)

    return mejor


def clave_candidata(estado: "EstadoPlan", enfermera: Enfermero) -> Tuple[int, int]:
    """
    Orden para candidatas: primero menos turnos totales, luego menos noches
    
    Parametros:
    estado : EstadoPlan
        Estado actual con contadores por persona
    enfermera : str
        Identificador de la persona candidata

    Retorna:
    Tuple[int, int]
        Tupla (total_turnos, total_noches) para orden ascendente
        donde valores menores se prueban antes

    Ejemplo:
    Si una enfermera tiene (3 turnos, 1 noche) y otra tiene (2 turnos, 0 noches),
    la segunda enfermera se prioriza
    """
    
    return (
        estado.total_turnos_por_enfermera[enfermera],
        estado.noches_por_enfermera[enfermera],
    )
