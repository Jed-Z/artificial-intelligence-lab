(define (problem prob)
    (:domain cube)

    (:objects
        w y g b r o - color  ; red, yellow, green, blue, red, orange
    )

    (:init
        (block1 w b r)
        (block2 y o b)
        (block3 r w g)
        (block4 g r y)
        (block5 y g o)
        (block6 o b w)
        (block7 y r b)
        (block8 w o g)
    )

    (:goal (and
        (block1 r w b)
        (block2 r y b)
        (block3 r w g)
        (block4 r y g)
        (block5 o w b)
        (block6 o y b)
        (block7 o w g)
        (block8 o y g)
    ))
)