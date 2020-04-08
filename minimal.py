# data simulated a week ago
r = pickle.load(open('simdata.pkl','rb'))
sr = sorted(r, key=lambda x: x['time'])

nb_humans = max([ev['human_id'] for ev in r]) + 1
risks = np.zeros([nb_humans])
for ev in sr:
    # update formulas
    me = ev['human_id']
    
    if ev['event_type']=='symptom_start':
        risks[me] += 0.5
        
    elif ev['event_type']=='test':
        if ev['payload']['result']:
            risks[me] = max(.8, risks[me])
        else:
            risks[me] = .1
            
    elif ev['event_type']=='encounter':
        you = ev['payload']['encounter_human_id']
        risks[me] += risks[you] * transmission_prob  # lenka
        # risks[me] = 1- (1- risks[me])*(1-transmission_prob* risks[you])  # yoshua
        
    risks[me] = min(1, risks[me])
    
print(risks)