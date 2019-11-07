(define (domain boxman)
    (:requirements :strips :typing :equality)
    (:types physob location)
    (:constants G - physob)  ; the guy（推箱子的人）

    (:predicates
        (at ?x - physob ?l - location)  ; 实体x在位置l
        (clear ?l - location)           ; 位置l上没有箱子，但可能有人
        (left ?l1 ?l2 - location)       ; 位置l1在l2的左边相邻
        (lower ?l1 ?l2 - location)      ; 位置l1在l2的下面相邻
    )

    (:action move  ; 推箱子的人从from走到to
        :parameters (?from ?to - location)
        :precondition (and
            (at G ?from)
            (clear ?to)
            (or  ; 四个方向之一相邻即可
                (left ?from ?to) (left ?to ?from)
                (lower ?from ?to) (lower ?to ?from)
            )
        )
        :effect (and
            (not (at G ?from))
            (at G ?to)
        )
    )

    (:action push  ; 推箱子的人目前在guypos，他把在from处的箱子推到位置to
        :parameters (?box - physob ?guypos ?from ?to - location)
        :precondition (and
            (not (= ?box G))
            (at ?box ?from)
            (at G ?guypos)
            (clear ?to)
            (or  ; 向四个方向中的一个推箱子
                (and (left ?guypos ?from) (left ?from ?to))    ; 向右推
                (and (left ?to ?from) (left ?from ?guypos))    ; 向左推
                (and (lower ?guypos ?from) (lower ?from ?to))  ; 向上推
                (and (lower ?to ?from) (lower ?from ?guypos))  ; 向下推
            )
        )
        :effect (and
            (not (at G ?guypos))
            (not (at ?box ?from))
            (clear ?from)      ; from现在空了
            (at G ?from)       ; 推箱子的人现在在from处
            (at ?box ?to)      ; 箱子现在在位置to处
            (not (clear ?to))  ; to上现在有箱子了
        )
    )
)
