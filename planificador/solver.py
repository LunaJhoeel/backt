from typing import List, Tuple, Optional, TYPE_CHECKING

from planificador.heuristicas import seleccionar_siguiente_dia_turno, clave_candidata
from planificador.restricciones import es_candidata
from planificador.constantes import TURNOS

if TYPE_CHECKING:
    from planificador.estado import EstadoPlan

Dia = str
Turno = str
Enfermero = str


class SolverBacktracking:
    """
    Ejecuta DFS recursivo con poda usando MRV y orden por carga
    """

    def __init__(self, estado: "EstadoPlan") -> None:
        self.estado: "EstadoPlan" = estado

    def asignar(self, enfermera: Enfermero, dia: Dia, turno: Turno) -> None:
        """
        Aplica efectos de asignar una persona a un turno
        """
        self.estado.plan[dia][turno].append(enfermera)
        self.estado.asignadas_por_dia[dia].add(enfermera)
        self.estado.total_turnos_por_enfermera[enfermera] += 1
        if turno == "N":
            self.estado.noches_por_enfermera[enfermera] += 1
        self.estado.dias_trabajados_por_enfermera[enfermera].add(dia)
        if self.estado.verbose:
            print(f"Asignar: {enfermera} -> {dia} {turno}")

    def desasignar(self, enfermera: Enfermero, dia: Dia, turno: Turno) -> None:
        """
        Revierte efectos de asignar para retroceso
        """
        if enfermera in self.estado.plan[dia][turno]:
            self.estado.plan[dia][turno].remove(enfermera)
        if enfermera in self.estado.asignadas_por_dia[dia]:
            self.estado.asignadas_por_dia[dia].remove(enfermera)
        self.estado.total_turnos_por_enfermera[enfermera] -= 1
        if turno == "N":
            self.estado.noches_por_enfermera[enfermera] -= 1
        if dia in self.estado.dias_trabajados_por_enfermera[enfermera]:
            self.estado.dias_trabajados_por_enfermera[enfermera].remove(dia)
        if self.estado.verbose:
            print(f"Retroceder: {enfermera} <- {dia} {turno}")

    def ordenar_candidatas(self, candidatas: List[Enfermero]) -> None:
        """
        Ordena candidatas segun clave_candidata
        """
        candidatas.sort(key=lambda enfermera: clave_candidata(self.estado, enfermera))

    def resolver(self) -> bool:
        """
        Resuelve mediante backtracking. Retorna True si se satisface toda la cobertura
        """
        self.estado.contador_recursiones += 1

        siguiente: Optional[Tuple[Dia, Turno]] = seleccionar_siguiente_dia_turno(self.estado)
        if siguiente is None:
            return True

        dia_actual, turno_actual = siguiente

        candidatas: List[Enfermero] = [
            e for e in self.estado.enfermeros
            if es_candidata(self.estado, e, dia_actual, turno_actual)
        ]

        self.ordenar_candidatas(candidatas)

        for e in candidatas:
            self.asignar(e, dia_actual, turno_actual)
            if self.resolver():
                return True
            self.estado.contador_retrocesos += 1
            self.desasignar(e, dia_actual, turno_actual)

        return False
