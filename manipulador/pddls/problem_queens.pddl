(define (problem four_queens-problem)
  (:domain four_queens)
  
  (:objects
    x1 x2 x3 x4 - position
    y1 y2 y3 y4 - position
    q1 q2 q3 q4 - queen
  )
  
  (:init
    ; All positions are initially safe
    (safe x1 y1) (safe x1 y2) (safe x1 y3) (safe x1 y4)
    (safe x2 y1) (safe x2 y2) (safe x2 y3) (safe x2 y4)
    (safe x3 y1) (safe x3 y2) (safe x3 y3) (safe x3 y4)
    (safe x4 y1) (safe x4 y2) (safe x4 y3) (safe x4 y4)

    ; Define attacks relationships
    (attacks x1 y1 x1 y2) (attacks x1 y1 x1 y3) (attacks x1 y1 x1 y4)
    (attacks x1 y1 x2 y1) (attacks x1 y1 x3 y1) (attacks x1 y1 x4 y1)
    (attacks x1 y1 x2 y2) (attacks x1 y1 x3 y3) (attacks x1 y1 x4 y4)

    (attacks x1 y2 x1 y3) (attacks x1 y2 x1 y4)
    (attacks x1 y2 x2 y2) (attacks x1 y2 x2 y3) (attacks x1 y2 x2 y4)
    (attacks x1 y2 x2 y1) (attacks x1 y2 x2 y3) (attacks x1 y2 x3 y4)

    (attacks x1 y3 x1 y4)
    (attacks x1 y3 x2 y3) (attacks x1 y3 x3 y3) (attacks x1 y3 x4 y3)
    (attacks x1 y3 x2 y4) (attacks x1 y3 x2 y2) (attacks x1 y3 x3 y1)

    (attacks x1 y4 x2 y4) (attacks x1 y4 x3 y4) (attacks x1 y4 x4 y4)
    (attacks x1 y4 x4 y1) (attacks x1 y4 x1 y3) (attacks x1 y4 x2 y2)

    (attacks x2 y1 x2 y2) (attacks x2 y1 x2 y3) (attacks x2 y1 x2 y4)
    (attacks x2 y1 x3 y1) (attacks x2 y1 x4 y1)
    (attacks x2 y1 x3 y2) (attacks x2 y1 x4 y3)

    (attacks x2 y2 x2 y3) (attacks x2 y2 x2 y4)
    (attacks x2 y2 x3 y2) (attacks x2 y2 x4 y2)
    (attacks x2 y2 x3 y3) (attacks x2 y2 x4 y4) (attacks x2 y2 x3 y2) 

    (attacks x2 y3 x2 y4)
    (attacks x2 y3 x3 y3) (attacks x2 y3 x4 y3)
    (attacks x2 y3 x3 y4) (attacks x2 y3 x4 y1) (attacks x2 y3 x3 y2) 

    (attacks x2 y4 x3 y4) (attacks x2 y4 x4 y4)
    (attacks x2 y4 x3 y3) (attacks x2 y4 x4 y2)

    (attacks x3 y1 x3 y2) (attacks x3 y1 x3 y3) (attacks x3 y1 x3 y4)
    (attacks x3 y1 x4 y1)
    (attacks x3 y1 x4 y2)

    (attacks x3 y2 x3 y3) (attacks x3 y2 x3 y4)
    (attacks x3 y2 x4 y2)
    (attacks x3 y2 x4 y3) (attacks x3 y2 x4 y1)

    (attacks x3 y3 x3 y4) 
    (attacks x3 y3 x4 y4)
    (attacks x3 y3 x4 y2) (attacks x3 y3 x4 y4)

    (attacks x3 y4 x4 y4)
    (attacks x3 y4 x4 y3)

    (attacks x4 y1 x4 y2) (attacks x4 y1 x4 y3) (attacks x4 y1 x4 y4)

    (attacks x4 y2 x4 y3) (attacks x4 y2 x4 y4)
    
    (attacks x4 y3 x4 y4)

  )
  
  (:goal
    (and
      (placed q1) (placed q2) 
      (placed q3) (placed q4)
    )
  )
)
