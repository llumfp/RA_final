
(define (problem queen_movement-problem)
  (:domain queen_movement)
  
  (:objects
    pos11 pos12 pos15 pos11h1 pos12h1 pos15h1 pos11h2 pos12h2 pos15h2 - cell
    rob - robot
    p11 p12 p15- piece
  )
  
  (:init
    ; Posiciones iniciales de las piezas
    (at p11 pos11) (at p12 pos12)(at p15 pos15)
    
    ; El robot empieza sin coger nada
    (free rob)
    
    (at rob pos11)
  )
  
  (:goal
    (and
     (at p11 12h1)
     (at p15 12h2)
    )
  )
)
