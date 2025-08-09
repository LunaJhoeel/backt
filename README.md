# Progamacion de turnos de enfermeria con Backtracking

## Que es
Programa que arma horarios semanales segun:
- dias de trabajo (Lun a Vie)
- cobertura por turno (M, T, N)
- disponibilidad por persona

Respeta limites basicos: nadie hace dos turnos el mismo dia, evita manana despues de noche, y limita turnos, noches y dias consecutivos por semana.

## Requisitos
- Python 3.11 o superior
- Sin librerias externas

## Estructura del proyecto
proyecto/
├─ main.py
└─ planificador/
├─ init.py
├─ constantes.py
├─ estado.py
├─ heuristicas.py
├─ restricciones.py
└─ solver.py
