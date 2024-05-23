(define (domain queen_movement)
  (:requirements :strips :typing :fluents :equality)

(:types cell floor - position
        robot piece - object

)

(:predicates
    (at ?o - object ?p - position)
    (grabbed ?r - robot ?p - piece)
    (free ?r - robot))


(:functions
    (height ?p - position)
)

(:action mover
    :parameters (?r - robot ?p1 - cell ?p2 - cell)
    :precondition (at ?r ?p1)
    :effect (and (not (at ?r ?p1)) (at ?r ?p2))
)

(:action pick
    :parameters (?r - robot ?p - piece ?pos - cell)
    :precondition (and (free ?r) (at ?r ?pos) (at ?p ?pos) (= (height ?pos) 1))
    :effect (and (grabbed ?r ?p) (not (free ?r)) (not (at ?p ?pos)) (decrease (height ?pos) 1))
)

(:action place
  :parameters (?r - robot ?p - piece ?pos - cell ?f - floor)
  :precondition (and (at ?r ?pos) (grabbed ?r ?p) (= (height ?pos) (height ?f)))
  :effect (and (free ?r) (not(grabbed ?r ?p)) (increase (height ?pos) 1))
)
  )