% -- Problem 1: Predicates, expressing that "A is the xxx of B".
grandchild(A,B):-child(A,C),child(C,B).
greatGrandparent(A,B):-child(B,D),child(D,C),child(C,A).
ancestor(A,B):-child(B,A).
ancestor(A,B):-child(C,A),ancestor(C,B).
brother(A,B):-male(A),mother(C,A),mother(C,B),A\=B.   % use `mother` to remove duplicates
sister(A,B):-female(A),mother(C,A),mother(C,B),A\=B.  % use `mother` to remove duplicates
daughter(A,B):-female(A),child(A,B).
son(A,B):-male(A),child(A,B).
firstCousin(A,B):-grandchild(A,C),grandchild(B,C),A\=B.
brotherInLaw(A,B):-male(A),spouse(A,C),sister(C,B).    % sister's husband
brotherInLaw(A,B):-brother(A,C),spouse(B,C).           % husband/wife's brother
sisterInLaw(A,B):-female(A),spouse(A,C),brother(C,B).  % brother's wife
sisterInLaw(A,B):-sister(A,C),(B,C).             % husband/wife's sister
aunt(A,B):-sister(A,C),child(B,C).
aunt(A,B):-sisterInLaw(A,C),child(B,C).
uncle(A,B):-brother(A,C),child(B,C).
uncle(A,B):-brotherInLaw(A,C),child(B,C).

% some helper predicates, defined by myself
mother(A,B):-female(A),child(B,A).
father(A,B):-male(A),child(B,A).
% spouse(A,B):-child(C,A),child(C,B),A\=B.  % this is not used because it causes dupilicates easily
spouse(A,B):-husb_or_wife(A,B);husb_or_wife(B,A).
sibling(A,B):-child(A,C),child(B,C),A\=B.


% -- Problem 2: mth cousin n times removed
distance(A,A,0).
distance(C,A,K):-child(C,B),distance(B,A,K1),K is K1+1.
mthCousinNremoved(A,B,M,N):-distance(A,C,M+1),distance(B,C,M+N+1).


% -- Problem 3: Basic facts
% define gender
male('George').
male('Philip').
male('Spencer').
male('Charles').
male('Mark').
male('Andrew').
male('Edward').
male('William').
male('Harry').
male('Peter').
male('James').
female('Mum').
female('Kydd').
female('Elizabeth').
female('Margaret').
female('Diana').
female('Anne').
female('Sarah').
female('Sophie').
female('Zara').
female('Beatrice').
female('Eugenie').
female('Louise').
% define child relationship
child('Elizabeth','George').
child('Elizabeth','Mum').
child('Margaret','George').
child('Margaret','Mum').
child('Diana','Spencer').
child('Diana','Kydd').
child('Charles','Elizabeth').
child('Charles','Philip').
child('Anne','Elizabeth').
child('Anne','Philip').
child('Andrew','Elizabeth').
child('Andrew','Philip').
child('Edward','Elizabeth').
child('Edward','Philip').
child('William','Diana').
child('William','Charles').
child('Harry','Diana').
child('Harry','Charles').
child('Peter','Anne').
child('Peter','Mark').
child('Zara','Anne').
child('Zara','Mark').
child('Beatrice','Andrew').
child('Beatrice','Sarah').
child('Eugenie','Andrew').
child('Eugenie','Sarah').
child('Louise','Edward').
child('Louise','Sophie').
child('James','Edward').
child('James','Sophie').
% define spouse relationship
husb_or_wife('George','Mum').
husb_or_wife('Spencer','Kydd').
husb_or_wife('Elizabeth','Philip').
husb_or_wife('Diana','Charles').
husb_or_wife('Anne','Mark').
husb_or_wife('Andrew','Sarah').
husb_or_wife('Edward','Sophie').
