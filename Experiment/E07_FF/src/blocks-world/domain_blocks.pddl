(define (domain blocks)
    (:requirements :strips :typing :equality :universal-preconditions :conditional-effects)
    (:types physob)  ; physical object

    (:predicates
        (ontable ?x - physob)  ; block `?x` is on the table
        (clear ?x - physob)    ; there is no block on top of `?x`
        (on ?x ?y - physob)    ; `?x` is on top of `?y`
    )

    (:action move  ; move `?x` to top of `?y`
        :parameters (?x ?y - physob)
        :precondition (and (clear ?x) (clear ?y) (not (= ?x ?y)))
        :effect (and
            (forall (?z - physob) (when (on ?x ?z) (clear ?z)))
            (on ?x ?y) (not (clear ?y))
        )
    )

    (:action moveToTable  ; move `?x` to the table
        :parameters (?x - physob)
        :precondition (and (clear ?x) (not (ontable ?x)))
        :effect (and
            (forall (?z - physob) (when (on ?x ?z) (clear ?z)))
            (ontable ?x)
        )
    )
)