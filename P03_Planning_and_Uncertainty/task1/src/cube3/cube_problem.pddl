(define (problem prob)
    (:domain cube)

    (:objects
        w y g b r o - color  ; red, yellow, green, blue, red, orange
    )

    (:init
        (block1 g r y)
        (block2 w o g)
        (block3 b y o)
        (block4 r w b)
        (block5 b o w)
        (block6 g y o)
        (block7 g w r)
        (block8 b r y)
    )

    (:goal (and
        (block1 b y r)
        (block2 b w r)
        (block3 b y o)
        (block4 b w o)
        (block5 g y r)
        (block6 g w r)
        (block7 g y o)
        (block8 g w o)
    ))
)