use_module(library(lists)).

% 规划器，参数一是所有变量的列表，参数二是初始状态，参数三是目标状态，参数四是规划的结果（即动作序列）
plan(Objects, Init, Goal, Result):- h(Objects, Init, Goal, 0, H_value), aStar(Objects, [[Init, [], 0, H_value]], Goal, [], Result).

% A*搜索，参数表：（变量列表，边界列表，目标状态，已访问的状态列表，搜索路径）
aStar(_, Frontier, Goal, _, Path) :- getMinQueue(Frontier, [[State,Path,_,_]|_]), sublist(Goal, State), !.
aStar(Objects, Frontier, Goal, Visited, Path):-
    getMinQueue(Frontier, [[State,Action_old,G,_]|Frontier_remain]),
    pushFront(State, Visited, Visited_new),
    G_new is G + 1,
    findall([MidState, Action_new, G_new, H_new], 
            validAction(Objects, MidState, Action_new, H_new, State, Goal, Action_old, Visited_new, G_new), 
            State_new),
    append(Frontier_remain, State_new, Frontier_new),
    aStar(Objects, Frontier_new, Goal, Visited_new, Path).

% 启发函数
h1(Objects, State, Goal, V1):- findall(X, (member(X, Objects), block(X), not(isGoal(X, State, Goal))), NotGoalList), length(NotGoalList, V1), !.
h2(Objects, State, Goal, V2):-
    findall(X, (block(X), member(X, Objects), not(isGoal(X, State, Goal)), below(Y, X, State), below(Y, X, Goal)), NotGoalList),
    length(NotGoalList, V2), !.
h(Objects, State, Goal, G, Value):- h1(Objects, State, Goal, V1), h2(Objects, State, Goal, V2), Value is V1 + V2 + G.

% 找到队列里H最小的状态
getMinQueue([H|T], Result) :- getMin(H, [], T, Result).
getMin(H, S, [], [H|S]).
getMin(C, S, [H|T], Result):- nth0(3,C,H1), nth0(3,H,H2), H1=<H2, !, getMin(C, [H|S], T, Result); getMin(H, [C|S], T, Result).

% 判断一个列表（参数一）是不是另一个列表（参数二）的子列
sublist([], _).
sublist([H|T], L2):- member(H, L2), sublist(T, L2).

% 把元素（参数一）插入到列表（参数二）头部，结果为第三个参数
pushFront(X, L2, [X|L2]).

% 把元素（参数一）插入到列表（参数二）尾部，结果为第三个参数
pushBack(X, [], [X]).
pushBack(X, [Y|T], [Y|T_new]):- pushBack(X, T, T_new).

% move动作的添加和删除状态
stripsAdd(move(Block, From, To), [clear(From), on(Block, To)]).
stripsDel(move(Block, From, To), [clear(To), on(Block, From)]).

deleteAll([], _, []).
deleteAll([X|L1], L2, Diff):- member(X, L2), !, deleteAll(L1, L2, Diff).
deleteAll([X|L1], L2, [X|Diff]):- deleteAll(L1, L2, Diff).

% 有效的动作
actionCond(Objects, move(Block,From,To), [clear(Block),clear(To),on(Block,From)]) :-
    block(Block), (block(From);table(From)), (block(To);table(To)),
    Block \= From, From \= To, To \= Block,
    member(Block, Objects), member(From, Objects), member(To, Objects).
getAction(Objects, State, Action):- actionCond(Objects, Action, Condition), sublist(Condition, State).

% 执行动作
doAction(State, Action, NewState):-
    stripsDel(Action, DelList), deleteAll(State, DelList, State1), !,
    stripsAdd(Action, AddList), append(AddList, State1, NewState).
validAction(Objects, MidState, Action_new, H_new, State, Goals, Action_old, Visited_new, G):-
    getAction(Objects, State, Action),  doAction(State, Action, MidState),
    not(member(MidState, Visited_new)), pushBack(Action, Action_old, Action_new),
    h(Objects, MidState, Goals, G, H_new).

% 判断参数一表示的积木是否在参数二表示的积木下
below(X, X, _).
below(X, Y, State):- block(X), block(Y), X \= Y, member(on(Z, X), State), below(Z, Y, State).

% 判断X是否在目标状态
isGoal(X, _, _):- table(X).
isGoal(X, State, Goal):- member(on(X,Y),State), member(on(X,Y),Goal), isGoal(Y,State,Goal).

% 测试样例的定义及封装
block(b1).
block(b2).
block(b3).
block(b4).
block(b5).
block(b6).
block(b7).
block(b8).
table(1).
table(2).
table(3).
table(4).
table(5).
table(6).
table(7).
table(8).

test_1:-
    plan([b1, b2, b3, 1, 2, 3],
        [clear(b2), on(b2, b1), on(b1, b3), on(b3, 1), clear(2), clear(3)],
        [clear(b3), on(b3, b1), on(b1, 1), clear(b2), on(b2, 2), clear(3)],
        Result), maplist(writeln, Result).
test_2:-
    plan([b1, b2, b3, b4, b5, 1, 2, 3, 4, 5],
        [clear(b1), on(b1, b5), on(b5, b2), on(b2, 1), clear(b3), on(b3, b4), on(b4, 2), clear(3), clear(4), clear(5)],
        [clear(1), clear(b2), on(b2, b1), on(b1, b3), on(b3, 2), clear(3), clear(b4), on(b4, b5), on(b5, 4), clear(5)],
        Result), maplist(writeln, Result).
test_3:-
    plan([b1, b2, b3, b4, b5, 1, 2, 3, 4, 5],
        [clear(b1), on(b1, b5), on(b5, b2), on(b2, 1), clear(b3), on(b3, b4), on(b4, 2), clear(3), clear(4), clear(5)],
        [clear(1), clear(b4), on(b4, b3), on(b3, b5), on(b5, b1), on(b1, b2), on(b2, 2), clear(3), clear(4), clear(5)],
        Result), maplist(writeln, Result).
test_4:-
    plan([b1, b2, b3, b4, b5, b6, 1, 2, 3, 4, 5, 6],
        [clear(b1), on(b1, 1), clear(2), clear(b6), on(b6, b2), on(b2, b3), on(b3, 3), clear(4), clear(b4), on(b4, b5), on(b5, 5), clear(6)],
        [clear(b6), on(b6, b2), on(b2, b4), on(b4, b1), on(b1, b3), on(b3, b5), on(b5, 1), clear(2), clear(3), clear(4), clear(5), clear(6)],
        Result), maplist(writeln, Result).
test_5:-
    plan([b1, b2, b3, b4, b5, b6, b7, b8, 1, 2, 3, 4, 5, 6, 7, 8],
        [clear(b1), on(b1, 1), clear(2), clear(b6), on(b6, b2), on(b2, b3), on(b3, 3), clear(4), clear(b4), on(b4, b5), on(b5, 5), clear(b8), on(b8, b7), on(b7, 6), clear(7), clear(8)],
        [clear(b7), on(b7, b2), on(b2, b4), on(b4, b1), on(b1, b3), on(b3, b6), on(b6, b8), on(b8, b5), on(b5, 1), clear(2), clear(3), clear(4), clear(5), clear(6), clear(7), clear(8)],
        Result), maplist(writeln, Result).
