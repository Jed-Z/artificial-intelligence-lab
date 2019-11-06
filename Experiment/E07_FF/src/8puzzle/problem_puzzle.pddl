(define (problem prob)
    (:domain puzzle)
    
    (:objects
        loc1 loc2 loc3 loc4 loc5 loc6 loc7 loc8 loc0 - location  ; locN means numN's target location
        num1 num2 num3 num4 num5 num6 num7 num8 num0 - number    ; num0 indicates the empty cell
    )

    (:init
        ; initial configuration
        (at num1 loc1) (at num5 loc2) (at num2 loc3)
        (at num7 loc4) (at num4 loc5) (at num3 loc6)
        (at num8 loc7) (at num0 loc8) (at num6 loc0)

        ; define neighbourhoods (one-way neighbour is enough here)
        (neighbour loc1 loc2) (neighbour loc2 loc3)
        (neighbour loc4 loc5) (neighbour loc5 loc6)
        (neighbour loc7 loc8) (neighbour loc8 loc0)
        (neighbour loc1 loc4) (neighbour loc4 loc7)
        (neighbour loc2 loc5) (neighbour loc5 loc8)
        (neighbour loc3 loc6) (neighbour loc6 loc0)
    )

    (:goal (and
        (at num1 loc1) (at num2 loc2) (at num3 loc3)
        (at num4 loc4) (at num5 loc5) (at num6 loc6)
        (at num7 loc7) (at num8 loc8) (at num0 loc0)
    ))
)
