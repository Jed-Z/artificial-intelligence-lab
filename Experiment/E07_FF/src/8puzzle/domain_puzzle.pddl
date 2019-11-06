(define (domain puzzle)
    (:requirements :strips :equality :typing)
    (:types number location)
    (:predicates
        (at ?n - number ?l - location)  ; indicates that the number `?n` is at location `?l`
        (neighbour ?l1 ?l2 - location)  ; indicates that `?l1` and `?l2` (or `?l2` and `?l1`) are neighbours
    )

    (:action slide  ; move the number `?num` from the cell `?from` to the cell `?to`
        :parameters (?num - number ?from ?to - location)
        :precondition (and
            (at ?num ?from)
            (at num0 ?to)
            (or (neighbour ?from ?to) (neighbour ?to ?from))
        )
        :effect (and
            (not (at num0 ?to))
            (at num0 ?from)
            (at ?num ?to)
        )
    )
)
