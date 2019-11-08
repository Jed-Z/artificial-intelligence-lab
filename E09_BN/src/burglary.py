from pomegranate import *
burglary = DiscreteDistribution({'T': 0.001, 'F': 0.999})
earthquake = DiscreteDistribution({'T': 0.002, 'F': 0.998})
alarm = ConditionalProbabilityTable([
    ['T', 'T', 'T', 0.95],
    ['T', 'T', 'F', 0.05],
    ['T', 'F', 'T', 0.94],
    ['T', 'F', 'F', 0.06],
    ['F', 'T', 'T', 0.29],
    ['F', 'T', 'F', 0.71],
    ['F', 'F', 'T', 0.001],
    ['F', 'F', 'F', 0.999],
], [burglary, earthquake])
johncalls = ConditionalProbabilityTable([
    ['T', 'T', 0.90],
    ['T', 'F', 0.10],
    ['F', 'T', 0.05],
    ['F', 'F', 0.95],
], [alarm])
marycalls = ConditionalProbabilityTable([
    ['T', 'T', 0.70],
    ['T', 'F', 0.30],
    ['F', 'T', 0.01],
    ['F', 'F', 0.99],
], [alarm])

sB = State(burglary, name='burglary')      # 0
sE = State(earthquake, name='earthquake')  # 1
sA = State(alarm, name='alarm')            # 2
sJ = State(johncalls, name='johncalls')    # 3
sM = State(marycalls, name='marycalls')    # 4

model = BayesianNetwork('Burglary Problem')
model.add_states(sB, sE, sA, sJ, sM)
model.add_transition(sB, sA)
model.add_transition(sE, sA)
model.add_transition(sA, sJ)
model.add_transition(sA, sM)
model.bake()

result1 = model.predict_proba({})[2].parameters[0]['T']
print('P(A) =', result1)
result2 = model.predict_proba({'marycalls': 'F'})[3].parameters[0]['T'] * model.predict_proba({})[4].parameters[0]['F']
print('P(J&&~M) =', result2)
result3 = model.predict_proba({'johncalls': 'T', 'marycalls': 'F'})[2].parameters[0]['T']
print('P(A|J&&~M) =', result3)
result4 = model.predict_proba({'alarm': 'T'})[0].parameters[0]['T']
print('P(B|A) =', result4)
result5 = model.predict_proba({'johncalls': 'T', 'marycalls': 'F'})[0].parameters[0]['T']
print('P(A|J&&~M) =', result5)
result6 = (result2 * (1-result5)) / model.predict_proba({})[0].parameters[0]['F']
print('P(J&&~M|~B) =', result6)