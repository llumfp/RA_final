(define (problem queen_movement-problem)
  (:domain queen_movement)
  
  (:objects
    pos1 pos2 - cell
    rob - robot
    p1 p2 - piece
    h0 h1 - floor

  )
  
  (:init
    ; Totes les peces colocades, cada una a la seva posició
    (at p1  pos1) 
    (at p2  pos2)
    
    ;el robot empieza sin coger nada
    (free rob)
    (at rob  pos2)


    ;empezamos que todos las posiciones estan en altura de 1 (porque hay una pieza)
    (= (height pos1) 1)
    (= (height pos2) 1)
  

    (= (height h0) 0)
    (= (height h1) 1)

    (at rob pos1)


  )
  
  (:goal
    (and
     (= (height pos1) 2)
    )
  )
)
