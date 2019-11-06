(define (problem prob)
    (:domain blocks)

    (:objects A B C D E F - physob)

    (:init
        (clear A) (on A B) (on B C) (ontable C)
        (clear E) (on E D) (ontable D)        
        (clear F) (ontable F)
    )

    (:goal (and
        (clear F) (on F A) (on A C) (ontable C)
        (clear E) (on E B) (on B D) (ontable D)
    ))
)