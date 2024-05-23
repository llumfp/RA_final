(define (domain four_queens)
  (:requirements :strips :typing)
  (:types position queen)
  
  (:predicates
    (attacks ?x1 ?y1 ?x2 ?y2 - position)
    (safe ?x ?y - position)
    (placed ?q -queen)
  )

  (:action place-queen
    :parameters (?x  - position ?y - position ?q - queen)
    :precondition (and (safe ?x ?y)(not (placed ?q)))
    :effect 
      (and 
        (placed ?q)
        (not (safe ?x ?y))
        (forall (?i ?j - position) 
          (when (or(attacks ?x ?y ?i ?j)(attacks ?i ?j ?x ?y)) 
            (not (safe ?i ?j))))
      )
  )
)