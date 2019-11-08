from pomegranate import *
PatientAge = DiscreteDistribution({
    '0-30': 0.10,
    '31-65': 0.30,
    '65+': 0.60
})
CTScanResult = DiscreteDistribution({
    'Ischemic Stroke': 0.7,
    'Hemmorraghic Stroke': 0.3
})
MRIScanResult = DiscreteDistribution({
    'Ischemic Stroke': 0.7,
    'Hemmorraghic Stroke': 0.3
})
Anticoagulants = DiscreteDistribution({
    'Used': 0.5,
    'Not used': 0.5
})

StrokeType = ConditionalProbabilityTable([
    ['Ischemic Stroke','Ischemic Stroke','Ischemic Stroke',0.8],
    ['Ischemic Stroke','Hemmorraghic Stroke','Ischemic Stroke',0.5],  
    ['Hemmorraghic Stroke','Ischemic Stroke','Ischemic Stroke',0.5],
    ['Hemmorraghic Stroke','Hemmorraghic Stroke','Ischemic Stroke',0], 

    ['Ischemic Stroke','Ischemic Stroke','Hemmorraghic Stroke',0],
    ['Ischemic Stroke','Hemmorraghic Stroke','Hemmorraghic Stroke',0.4], 
    ['Hemmorraghic Stroke','Ischemic Stroke','Hemmorraghic Stroke',0.4],
    ['Hemmorraghic Stroke','Hemmorraghic Stroke','Hemmorraghic Stroke',0.9],

    ['Ischemic Stroke','Ischemic Stroke','Stroke Mimic',0.2],
    ['Ischemic Stroke','Hemmorraghic Stroke','Stroke Mimic',0.1],    
    ['Hemmorraghic Stroke','Ischemic Stroke','Stroke Mimic',0.1],
    ['Hemmorraghic Stroke','Hemmorraghic Stroke','Stroke Mimic',0.1]
], [CTScanResult, MRIScanResult])

Mortality = ConditionalProbabilityTable([
    ['Ischemic Stroke', 'Used', 'False',0.28],
    ['Hemmorraghic Stroke', 'Used', 'False',0.99],
    ['Stroke Mimic', 'Used', 'False',0.1],
    ['Ischemic Stroke','Not used', 'False',0.56],
    ['Hemmorraghic Stroke', 'Not used', 'False',0.58],
    ['Stroke Mimic', 'Not used', 'False',0.05],

    ['Ischemic Stroke',  'Used' ,'True',0.72],
    ['Hemmorraghic Stroke', 'Used', 'True',0.01],
    ['Stroke Mimic', 'Used', 'True',0.9],
    ['Ischemic Stroke',  'Not used' ,'True',0.44],
    ['Hemmorraghic Stroke', 'Not used', 'True',0.42 ],
    ['Stroke Mimic', 'Not used', 'True',0.95]
], [StrokeType, Anticoagulants])

Disability = ConditionalProbabilityTable([
    ['Ischemic Stroke',   '0-30','Negligible', 0.80],
    ['Hemmorraghic Stroke', '0-30','Negligible', 0.70],
    ['Stroke Mimic',        '0-30', 'Negligible',0.9],
    ['Ischemic Stroke',     '31-65','Negligible', 0.60],
    ['Hemmorraghic Stroke', '31-65','Negligible', 0.50],
    ['Stroke Mimic',        '31-65', 'Negligible',0.4],
    ['Ischemic Stroke',     '65+'  , 'Negligible',0.30],
    ['Hemmorraghic Stroke', '65+'  , 'Negligible',0.20],
    ['Stroke Mimic',        '65+'  , 'Negligible',0.1],

    ['Ischemic Stroke',     '0-30' ,'Moderate',0.1],
    ['Hemmorraghic Stroke', '0-30' ,'Moderate',0.2],
    ['Stroke Mimic',        '0-30' ,'Moderate',0.05],
    ['Ischemic Stroke',     '31-65','Moderate',0.3],
    ['Hemmorraghic Stroke', '31-65','Moderate',0.4],
    ['Stroke Mimic',        '31-65','Moderate',0.3],
    ['Ischemic Stroke',     '65+'  ,'Moderate',0.4],
    ['Hemmorraghic Stroke', '65+'  ,'Moderate',0.2],
    ['Stroke Mimic',        '65+'  ,'Moderate',0.1],

    ['Ischemic Stroke',     '0-30' ,'Severe',0.1],
    ['Hemmorraghic Stroke', '0-30' ,'Severe',0.1],
    ['Stroke Mimic',        '0-30' ,'Severe',0.05],
    ['Ischemic Stroke',     '31-65','Severe',0.1],
    ['Hemmorraghic Stroke', '31-65','Severe',0.1],
    ['Stroke Mimic',        '31-65','Severe',0.3],
    ['Ischemic Stroke',     '65+'  ,'Severe',0.3],
    ['Hemmorraghic Stroke', '65+'  ,'Severe',0.6],
    ['Stroke Mimic',        '65+'  ,'Severe',0.8]
], [StrokeType, PatientAge])

sPA = State(PatientAge, name='PatientAge')         # 0
sCT = State(CTScanResult, name='CTScanResult')     # 1
sMR = State(MRIScanResult, name='MRIScanResult')   # 2
sAN = State(Anticoagulants, name='Anticoagulants') # 3
sDI = State(Disability, name='Disability')         # 4
sST = State(StrokeType, name='StrokeType')         # 5
sMO = State(Mortality, name='Mortality')           # 6

model = BayesianNetwork('Diagnosing')
model.add_states(sPA, sCT, sMR, sAN, sDI, sST, sMO)
model.add_transition(sPA, sDI)
model.add_transition(sCT, sST)
model.add_transition(sMR, sST)
model.add_transition(sAN, sMO)
model.add_transition(sST, sDI)
model.add_transition(sST, sMO)
model.bake()

result1 = model.predict_proba({'PatientAge': '31-65', 'CTScanResult': 'Ischemic Stroke'})[6].parameters[0]['True']
print('p1 = {:.5f}'.format(result1))
result2 = model.predict_proba({'PatientAge': '65+', 'MRIScanResult': 'Hemmorraghic Stroke'})[4].parameters[0]['Moderate']
print('p2 = {:.2f}'.format(result2))
result3 = model.predict_proba({'PatientAge': '65+', 'CTScanResult': 'Hemmorraghic Stroke', 'MRIScanResult': 'Ischemic Stroke'})[5].parameters[0]['Stroke Mimic']
print('p3 = {:.1f}'.format(result3))
result4 = model.predict_proba({'PatientAge': '0-30'})[3].parameters[0]['Not used']
print('p4 = {:.1f}'.format(result4))