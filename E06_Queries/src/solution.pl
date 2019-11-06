% 1
setof(X, branch(X,beigang), Result).

% 2
assertz((categoryDistrict(C,D):-restaurant(R,,C),branch(R,A), district(A,Dist))).
setof(D, (categoryDistrict(yuecai,D),categoryDistrict(xiangcai,D)), Result).

% 3
setof(
        R,
        Count^As^CountList^(
            findall(
                Counts,
                setof(
                    Count,
                    As^( restaurant(R,_,_), setof(A,branch(R,A),As), length(As,Count)),
                    Counts
                ),
                CountList
            ),
            min_list(CountList, MinCount), setof(A,branch(R,A),As), length(As,Count), Count = MinCount
            ),
            Result
    ).

% 4
setof(
    A,
    Count^ Rs^ (
        setof(R, branch(R,A), Rs),
        length(Rs, Count), Count>=2
    ),
    Result
).

% 5
setof(
    R,
    YearList^(
        findall(
            Ys,
            setof(Y,C^restaurant(R,Y,C),Ys),
            YearList
        ), min_list(YearList, MinYear), restaurant(R,Y,_), Y = MinYear
    ),
    Result
).

% 6
setof(
    R,
    Count^ As^ (
        setof(A, (branch(R,A)), As),
        length(As, Count), Count>=10
    ),
    Result
).


% 7
assertz((sameDistrict(R1,R2):-branch(R1,A1),branch(R2,A2),district(A1,D),district(A2,D),R1\=R2)).
assertz((printList([]))).
assertz((printList([H|T]):-write(H),nl,printList(T))).
findall(Res,setof(L,(restaurant(R,_,_),setof(B,branch(R,B),Bran),length(Bran,L)),Res),List);
