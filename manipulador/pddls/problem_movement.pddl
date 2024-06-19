
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
     (= (height pos3) 4)
     (= (height pos5) 4)
     (= (height pos12) 4)
     (= (height pos14) 4)
    )
  )
)
