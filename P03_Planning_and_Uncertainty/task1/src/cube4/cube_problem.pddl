(define (problem prob)
    (:domain cube)

    (:objects
        w y g b r o - color  ; red, yellow, green, blue, red, orange
    )

    (:init
        (block1 y b o)
        (block2 g w o)
        (block3 w b o)
        (block4 w r g)
        (block5 r g y)
        (block6 g y o)
        (block7 r b y)
        (block8 w r b)
    )

    (:goal (and
        (block1 w b r)
        (block2 w g r)
        (block3 w b o)
        (block4 w g o)
        (block5 y b r)
        (block6 y g r)
        (block7 y b o)
        (block8 y g o)
    ))
)