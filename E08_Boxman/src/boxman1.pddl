(define (problem prob)
    (:domain boxman)

    (:objects
        P52 P53 P24 P34 P44 P54 P45 P55 P65 P75 P46 P47 - location
        BOX1 BOX2 BOX3 BOX4 - physob
    )

    (:init
        (at BOX1 P53)
        (at BOX2 P44)
        (at BOX3 P45)
        (at BOX4 P65)
        (at G P54) (clear P54)
        (clear P52)
        (clear P24)
        (clear P34)
        (clear P54)
        (clear P55)
        (clear P75)
        (clear P46)
        (clear P47)

        (left P24 P34)
        (left P34 P44)
        (left P44 P54)
        (left P45 P55)
        (left P55 P65)
        (left P65 P75)
        (lower P44 P45)
        (lower P45 P46)
        (lower P46 P47)
        (lower P52 P53)
        (lower P53 P54)
        (lower P54 P55)
    )

    (:goal (and
        (not (clear P52))
        (not (clear P24))
        (not (clear P47))
        (not (clear P75))
    ))
)