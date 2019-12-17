(define (domain cube)
    (:requirements :strips :typing :equality)
    (:types color)

    (:predicates
        ; 8个谓词表示魔方的8个角块（二阶魔方没有棱块）。参数顺序：上下、左右、前后
        (block1 ?d ?l ?f - color) ; 底层左前块
        (block2 ?d ?r ?f - color) ; 底层右前块
        (block3 ?d ?l ?b - color) ; 底层左后块
        (block4 ?d ?r ?b - color) ; 底层右后块
        (block5 ?u ?l ?f - color) ; 顶层左前块
        (block6 ?u ?r ?f - color) ; 顶层右前块
        (block7 ?u ?l ?b - color) ; 顶层左后块
        (block8 ?u ?r ?b - color) ; 顶层右后块
    )

    ; 共6个动作，分别对应魔方的6个面顺时针旋转90°。
    ; 每个动作会影响对应面的4个角块

    (:action R  ; 右边顺时针旋转90°
        :effect (and
            (forall (?d ?r ?f - color)  ; 2->6
                (when (block2 ?d ?r ?f)
                    (and
                        (block6 ?f ?r ?d)
                        (not (block2 ?d ?r ?f))
                    )
                )
            )
            (forall (?u ?r ?f - color)  ; 6->8
                (when (block6 ?u ?r ?f)
                    (and
                        (block8 ?f ?r ?u)
                        (not (block6 ?u ?r ?f))
                    )
                )
            )
            (forall (?u ?r ?b - color)  ; 8->4
                (when (block8 ?u ?r ?b)
                    (and
                        (block4 ?b ?r ?u)
                        (not (block8 ?u ?r ?b))
                    )
                )
            )
            (forall (?d ?r ?b - color)  ; 4->2
                (when (block4 ?d ?r ?b)
                    (and
                        (block2 ?b ?r ?d)
                        (not (block4 ?d ?r ?b))
                    )
                )
            )
        )
    )

    (:action U  ; 顶层顺时针旋转90°
        :effect (and
            (forall (?u ?l ?f - color)  ; 5->7
                (when (block5 ?u ?l ?f)
                    (and
                        (block7 ?u ?f ?l)
                        (not (block5 ?u ?l ?f))
                    )
                )
            )
            (forall (?u ?l ?b - color)  ; 7->8
                (when (block7 ?u ?l ?b)
                    (and
                        (block8 ?u ?b ?l)
                        (not (block7 ?u ?l ?b))
                    )
                )
            )
            (forall (?u ?r ?b - color)  ; 8->6
                (when (block8 ?u ?r ?b)
                    (and
                        (block6 ?u ?b ?r)
                        (not (block8 ?u ?r ?b))
                    )
                )
            )
            (forall (?u ?r ?f - color)  ; 6->5
                (when (block6 ?u ?r ?f)
                    (and
                        (block5 ?u ?f ?r)
                        (not (block6 ?u ?r ?f))
                    )
                )
            )
        )
    )

    (:action F  ; 前面顺时针旋转90°
        :effect (and
            (forall (?d ?l ?f - color)  ; 1->5
                (when (block1 ?d ?l ?f)
                    (and
                        (block5 ?l ?d ?f)
                        (not (block1 ?d ?l ?f))
                    )
                )
            )
            (forall (?u ?l ?f - color)  ; 5->6
                (when (block5 ?u ?l ?f)
                    (and
                        (block6 ?l ?u ?f)
                        (not (block5 ?u ?l ?f))
                    )
                )
            )
            (forall (?u ?r ?f - color)  ; 6->2
                (when (block6 ?u ?r ?f)
                    (and
                        (block2 ?r ?u ?f)
                        (not (block6 ?u ?r ?f))
                    )
                )
            )
            (forall (?d ?r ?f - color)  ; 2->1
                (when (block2 ?d ?r ?f)
                    (and
                        (block1 ?r ?d ?f)
                        (not (block2 ?d ?r ?f))
                    )
                )
            )
        )
    )

    (:action R_CCW  ; 右边逆时针旋转90°
        :effect (and
            (forall (?u ?r ?f - color)  ; 6->2
                (when (block6 ?u ?r ?f)
                    (and
                        (block2 ?f ?r ?u)
                        (not (block6 ?u ?r ?f))
                    )
                )
            )
            (forall (?d ?r ?f - color)  ; 2->4
                (when (block2 ?d ?r ?f)
                    (and
                        (block4 ?f ?r ?d)
                        (not (block2 ?d ?r ?f))
                    )
                )
            )
            (forall (?d ?r ?b - color)  ; 4->8
                (when (block4 ?d ?r ?b)
                    (and
                        (block8 ?b ?r ?b)
                        (not (block4 ?d ?r ?b))
                    )
                )
            )
            (forall (?u ?r ?b - color)  ; 8->6
                (when (block8 ?u ?r ?b)
                    (and
                        (block6 ?b ?r ?u)
                        (not (block8 ?u ?r ?b))
                    )
                )
            )
        )
    )

    (:action U_CCW  ; 顶层逆时针旋转90°
        :effect (and
            (forall (?u ?r ?f - color)  ; 6->8
                (when (block6 ?u ?r ?f)
                    (and
                        (block8 ?u ?f ?r)
                        (not (block6 ?u ?r ?f))
                    )
                )
            )
            (forall (?u ?r ?b - color)  ; 8->7
                (when (block8 ?u ?r ?b)
                    (and
                        (block7 ?u ?b ?r)
                        (not (block8 ?u ?r ?b))
                    )
                )
            )
            (forall (?u ?l ?b - color)  ; 7->5
                (when (block7 ?u ?l ?b)
                    (and
                        (block5 ?u ?b ?l)
                        (not (block7 ?u ?l ?b))
                    )
                )
            )
            (forall (?u ?l ?f - color)  ; 5->6
                (when (block5 ?u ?l ?f)
                    (and
                        (block6 ?u ?f ?l)
                        (not (block5 ?u ?l ?f))
                    )
                )
            )
        )
    )

    (:action F_CCW  ; 前面逆时针旋转90°
        :effect (and
            (forall (?d ?l ?f - color)  ; 1->2
                (when (block1 ?d ?l ?f)
                    (and
                        (block2 ?l ?d ?f)
                        (not (block1 ?d ?l ?f))
                    )
                )
            )
            (forall (?d ?r ?f - color)  ; 2->6
                (when (block2 ?d ?r ?f)
                    (and
                        (block6 ?r ?d ?f)
                        (not (block2 ?d ?r ?f))
                    )
                )
            )
            (forall (?u ?r ?f - color)  ; 6->5
                (when (block6 ?u ?r ?f)
                    (and
                        (block5 ?r ?u ?f)
                        (not (block6 ?u ?r ?f))
                    )
                )
            )
            (forall (?u ?l ?f - color)  ; 5->1
                (when (block5 ?u ?l ?f)
                    (and
                        (not (block5 ?u ?l ?f))
                        (block1 ?l ?u ?f)
                    )
                )
            )
        )
    )
)
