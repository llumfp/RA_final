(define (domain queen_movement_nofluents)
  (:requirements :strips :typing :equality)

(:types cell air - position
        robot piece - object
)

(:predicates
    (at ?o - piece ?p - position)
    (grabbed ?r - robot ?p - piece)
    (free ?r - robot)
    (occupied ?p - position)
    (topof ?p - position ?p -position))

(:action pick
    :parameters (?r - robot ?p - piece ?pos - cell ?pos2 - position)
    :precondition (and (free ?r) (at ?p ?pos) (topof ?pos2 ?pos) (not (occupied ?pos2)))
    :effect (and (grabbed ?r ?p) (not (free ?r)) (not (at ?p ?pos)) (not(occupied ?pos)))
)

(:action place
  :parameters (?r - robot ?p - piece ?pos - cell ?pos2 - cell)
  :precondition (and (grabbed ?r ?p) (topof ?pos ?pos2) (occupied ?pos2) (not(occupied ?pos)))
  :effect (and (free ?r) (not(grabbed ?r ?p)) (at ?p ?pos) (occupied ?pos))
))
