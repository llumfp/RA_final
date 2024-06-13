
(define (problem queen_movement-problem)
  (:domain queen_movement)
  
  (:objects
    pos1 pos2 pos3 pos4- cell
    rob - robot
    p1 p2 p3- piece
  )
  
  (:init
    ; Posiciones iniciales de las piezas
    (at p1 pos1) (at p2 pos2)  (at p3 pos3)
    
    ; El robot empieza sin coger nada
    (free rob)
    
    (at rob pos1)
  )
  
  (:goal
    (and
     (at p1 pos3)
     (at p3 pos4)
    )
  )
)
