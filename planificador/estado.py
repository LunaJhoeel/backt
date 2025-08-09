from typing import Dict, List, Set, Tuple, Sequence, DefaultDict
from collections import defaultdict
from planificador.constantes import TURNOS

Dia = str
Turno = str
Enfermero = str

Plan = Dict[Dia, Dict[Turno, List[Enfermero]]]
Cobertura = Dict[Dia, Dict[Turno, int]]
Disponibilidad = Dict[Enfermero, Set[Tuple[Dia, Turno]]]


class EstadoPlan:
    """
    Mantiene el estado cambiante del planificador durante la busqueda
    """

    def __init__(
        self,
        dias: Sequence[Dia],
        enfermeros: Sequence[Enfermero],
        cobertura: Cobertura,
        disponibilidad: Disponibilidad,
        max_turnos_semana: int,
        max_noches_semana: int,
        max_dias_consecutivos: int,
        verbose: bool,
    ) -> None:
        """
        Construye estructuras y contadores internos
        """
        # Entradas
        self.dias: List[Dia] = list(dias)
        self.enfermeros: List[Enfermero] = list(enfermeros)
        self.cobertura: Cobertura = cobertura
        self.disponibilidad: Disponibilidad = disponibilidad
        
        self.plan: Plan = {d: {t: [] for t in TURNOS} for d in self.dias}
        
        # Impide que una persona tome 2 turnos el mismo dia
        self.asignadas_por_dia: Dict[Dia, Set[Enfermero]] = {d: set() for d in self.dias}

        # Contadores por persona
        self.total_turnos_por_enfermera: DefaultDict[Enfermero, int] = defaultdict(int)
        self.noches_por_enfermera: DefaultDict[Enfermero, int] = defaultdict(int)
        self.dias_trabajados_por_enfermera: DefaultDict[Enfermero, Set[Dia]] = defaultdict(set)

        # Permite ubicar el dia para verificar condicion manana despues de noche anterior
        self.indice_por_dia: Dict[Dia, int] = {d: i for i, d in enumerate(self.dias)}
        
        # Por enfermero y por dia, se crea un conjunto set con los turnos que puede hacer
        self.dominio_disponibilidad: Dict[Tuple[Enfermero, Dia], Set[Turno]] = {
            (e, d): {t for t in TURNOS if e in self.disponibilidad and (d, t) in self.disponibilidad[e]}
            for e in self.enfermeros
            for d in self.dias
        }

        # Politicas del hospital
        self.max_turnos_semana: int = int(max_turnos_semana)
        self.max_noches_semana: int = int(max_noches_semana)
        self.max_dias_consecutivos: int = int(max_dias_consecutivos)

        # Metricas
        self.contador_recursiones: int = 0
        self.contador_retrocesos: int = 0
        self.verbose: bool = bool(verbose)
