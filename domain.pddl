(define (domain 4queens)
  (:requirements :strips :typing)
  (:types position)
  
  (:predicates
    (queen-at ?x ?y - position)
    (attacks ?x1 ?y1 ?x2 ?y2 - position)
    (safe ?x ?y - position)
  )

  (:action place-queen
    :parameters (?x ?y - position)
    :precondition 
      (and (safe ?x ?y))
    :effect 
      (and 
        (queen-at ?x ?y)
        (forall (?i ?j - position) 
          (when (attacks ?x ?y ?i ?j) 
            (not (safe ?i ?j))))
      )
  )
)