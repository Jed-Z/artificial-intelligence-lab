(define (problem prob)
    (:domain cube)

    (:objects
        w y g b r o - color  ; red, yellow, green, blue, red, orange
    )

    (:init
        (block1 y b o)
        (block2 w g r)
        (block3 b r y)
        (block4 w o b)
        (block5 g o y)
        (block6 w b r)
        (block7 g o w)
        (block8 g y r)
    )

    (:goal (and
        (block1 b r w)
        (block2 b o w)
        (block3 b r y)
        (block4 b o y)
        (block5 g r w)
        (block6 g o w)
        (block7 g r y)
        (block8 g o y)
    ))
)