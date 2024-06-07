import subprocess
import re

# Paso 1: Ejecutar el problema inicial y guardar el output
subprocess.run(['.\metricff.exe', '-o', 'domain_queens.pddl', '-f', 'problem_queens.pddl', '-O'], stdout=open('output.txt', 'w'))

# Paso 2: Leer el output.txt y extraer las acciones
with open('output.txt', 'r') as file:
    output_content = file.readlines()
moves = output_content[-14:-10]
moves_clean = [x[:-2].split()[-3:-1] for x in moves]

template = """
(define (problem queen_movement-problem)
  (:domain queen_movement)
  
  (:objects
    pos1 pos2 pos3 pos4 pos5 pos6 pos7 pos8 pos9 pos10 pos11 pos12 pos13 pos14 pos15 pos16 - cell
    rob - robot
    p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16 - piece
    h0 h1 h2 h3 - floor
  )
  
  (:init
    ; Posiciones iniciales de las piezas
    (at p1 pos1) (at p2 pos2) (at p3 pos3) (at p4 pos4) (at p5 pos5) (at p6 pos6)
    (at p7 pos7) (at p8 pos8) (at p9 pos9) (at p10 pos10) (at p11 pos11) (at p12 pos12)
    (at p13 pos13) (at p14 pos14) (at p15 pos15) (at p16 pos16)
    
    ; El robot empieza sin coger nada
    (free rob)
    
    ; Alturas iniciales de las posiciones
    (= (height pos1) 1) (= (height pos2) 1) (= (height pos3) 1) (= (height pos4) 1)
    (= (height pos5) 1) (= (height pos6) 1) (= (height pos7) 1) (= (height pos8) 1)
    (= (height pos9) 1) (= (height pos10) 1) (= (height pos11) 1) (= (height pos12) 1)
    (= (height pos13) 1) (= (height pos14) 1) (= (height pos15) 1) (= (height pos16) 1)
    
    (= (height h0) 0) (= (height h1) 1) (= (height h2) 2) (= (height h3) 3)
    
    (at rob pos1)
  )
  
  (:goal
    (and
"""


# Añadimos las acciones como condiciones de objetivo
goal_conditions = []
for action in moves_clean:
    x, y = action
    pos_index = (int(x[1]) - 1) * 4 + int(y[1])
    goal_conditions.append(f"(= (height pos{pos_index}) 4)")

template += "     " + "\n     ".join(goal_conditions) + "\n    )\n  )\n)\n"

# Paso 4: Guardar el nuevo archivo problem_movement.pddl
with open('problem_movement.pddl', 'w') as file:
    file.write(template)

subprocess.run(['.\metricff.exe', '-o', 'domain_movement.pddl', '-f', 'problem_movement.pddl', '-O'], stdout=open('output_movement.txt', 'w'))
