# Progamacion de turnos de enfermeria con Backtracking

Programa que arma horarios semanales segun:
- dias de trabajo (Lun a Vie)
- cobertura por turno (M, T, N)
- disponibilidad por persona
- nadie hace dos turnos el mismo dia 
- evita manana despues de noche
- limita turnos, noches y dias consecutivos por semana.

## Requisitos
- Python 3.11 o superior
- Sin librerias externas

## Integrantes
LUNA ACOSTUPA JHOEEL EDDYE 
GUEVARA VARGAS VICTOR MANUEL
NEIRA CHALAN JAVIER EDUARDO 
SOTO CHAMBILLA ALONSO GABRIEL 
VILCA PANTIGOSO KAROL BERLIZ

## Estructura del proyecto
proyecto/
├─ main.py
└─ planificador/
├─── init.py
├─── constantes.py
├─── estado.py
├─── heuristicas.py
├─── restricciones.py
└─── solver.py
