(define (problem queen_movement_nofluents-problem)
  (:domain queen_movement_nofluents)

(:objects
    pos1 pos2 pos3 pos4 pos5 pos6 pos7 pos8 pos9 - cell
    air1 air2 air3 - air
    rob - robot
    p1 p2 p3 - piece
  )

(:init
    ;altura

    (topof pos4 pos1) (topof pos7 pos4) (topof air1 pos7)
    (topof pos5 pos2) (topof pos8 pos5) (topof air2 pos8)
    (topof pos6 pos3) (topof pos9 pos6) (topof air3 pos9)

    ; Posiciones iniciales de las piezas
    (at p1 pos1) (at p2 pos2)  (at p3 pos3)
    
    ; El robot empieza sin coger nada
    (free rob)
    
    (occupied pos1)
    (occupied pos2)
    (occupied pos3)
  )

(:goal
     (occupied pos9)
    
  )
)