from typing import Dict, List, Set, Tuple, Sequence
import unittest

from planificador.constantes import TURNOS
from planificador.estado import EstadoPlan
from planificador.solver import SolverBacktracking

Dia = str
Turno = str
Enfermero = str

Cobertura = Dict[Dia, Dict[Turno, int]]
Disponibilidad = Dict[Enfermero, Set[Tuple[Dia, Turno]]]


def construir_cobertura(dias: Sequence[Dia], m: int, t: int, n: int) -> Cobertura:
    """
    Crea una cobertura uniforme por dia.
    """
    return {d: {"M": int(m), "T": int(t), "N": int(n)} for d in dias}


class TestPlanificador(unittest.TestCase):

    def test_solver_falla_por_noches_cero(self) -> None:
        """
        Si max_noches_semana es cero y hay demanda de noches, no debe haber solucion
        """
        dias: List[Dia] = ["Lun", "Mar", "Mie"]
        enfermeros: List[Enfermero] = ["Ana", "Luisa"]
        cobertura: Cobertura = construir_cobertura(dias, 1, 0, 1)

        disponibilidad: Disponibilidad = {
            "Ana": {
                ("Lun", "M"), ("Lun", "T"), ("Lun", "N"),
                ("Mar", "M"), ("Mar", "T"),
                ("Mie", "M"), ("Mie", "T"),
            },
            "Luisa": {
                ("Lun", "M"), ("Lun", "T"), ("Lun", "N"),
                ("Mar", "M"), ("Mar", "T"), ("Mar", "N"),
                ("Mie", "M"), ("Mie", "T"), ("Mie", "N"),
            },
        }

        estado = EstadoPlan(
            dias=dias,
            enfermeros=enfermeros,
            cobertura=cobertura,
            disponibilidad=disponibilidad,
            max_turnos_semana=5,
            max_noches_semana=0,
            max_dias_consecutivos=4,
            verbose=False,
        )
        solver = SolverBacktracking(estado)
        exito: bool = solver.resolver()
        self.assertFalse(exito, "El solver no debio encontrar plan con noches prohibidas")

    def test_regla_manana_despues_de_noche(self) -> None:
        """
        Quien trabaje noche un dia no debe tomar manana del dia siguiente.
        Diseno un caso minimal para forzar la regla.
        """
        dias: List[Dia] = ["Lun", "Mar"]
        enfermeros: List[Enfermero] = ["A", "B"]

        cobertura: Cobertura = {
            "Lun": {"M": 0, "T": 0, "N": 1},
            "Mar": {"M": 1, "T": 0, "N": 0},
        }

        disponibilidad: Disponibilidad = {
            "A": {("Lun", "N"), ("Mar", "M")},
            "B": {("Mar", "M")},
        }

        estado = EstadoPlan(
            dias=dias,
            enfermeros=enfermeros,
            cobertura=cobertura,
            disponibilidad=disponibilidad,
            max_turnos_semana=5,
            max_noches_semana=2,
            max_dias_consecutivos=4,
            verbose=False,
        )
        solver = SolverBacktracking(estado)
        exito: bool = solver.resolver()
        self.assertTrue(exito, "El caso minimo deberia ser posible")

        asignados_mar_m: List[Enfermero] = estado.plan["Mar"]["M"]
        self.assertIn("B", asignados_mar_m)
        self.assertNotIn("A", asignados_mar_m)


if __name__ == "__main__":
    unittest.main()
