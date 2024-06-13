(define (domain queen_movement)
  (:requirements :strips :typing :equality)

(:types cell - position
        robot piece - object

)

(:predicates
    (at ?o - object ?p - position)
    (grabbed ?r - robot ?p - piece)
    (free ?r - robot)
    (occupied ?p - position)
    (over ?posi1 - position ?posi2 - position))
    


(:action mover
    :parameters (?r - robot ?p1 - cell ?p2 - cell)
    :precondition (at ?r ?p1)
    :effect (and (not (at ?r ?p1)) (at ?r ?p2))
)

(:action pick
    :parameters (?r - robot ?p - piece ?pos - cell)
    :precondition (and (free ?r) (at ?r ?pos) (at ?p ?pos))
    :effect (and (grabbed ?r ?p) (not (free ?r)) (not (at ?p ?pos))(not(occupied ?pos)))
)

(:action place
  :parameters (?r - robot ?p - piece ?pos - cell ?f - floor)
  :precondition (and (at ?r ?pos) (grabbed ?r ?p) (not(occupied ?pos)))
  :effect (and (free ?r) (not(grabbed ?r ?p)) (occupied ?pos))
)
  )