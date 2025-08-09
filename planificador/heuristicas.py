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

            # MRV aplicado: se elige el (dia, turno) con la menor cantidad de candidatas
            if len(candidatas) < minimo:
                minimo = len(candidatas)
                mejor = (d, t)

    return mejor


def clave_candidata(estado: "EstadoPlan", enfermera: Enfermero) -> Tuple[int, int]:
    """
    Orden para candidatas: primero menos turnos totales, luego menos noches
    """
    return (
        estado.total_turnos_por_enfermera[enfermera],
        estado.noches_por_enfermera[enfermera],
    )
