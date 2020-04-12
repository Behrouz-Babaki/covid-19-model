import numpy as np
import pandas as pd
import datetime
import pickle

data = pickle.load(open("./data.pkl",'rb'))

class get_data():
    
    def __init__(self, data):
        self.c_data = data
        self.data = self.clean_data()
        
    def clean_data(self):
        for d in range(len(data)-1, -1, -1):
            if data[d]['event_type'] != 'encounter':
                data.pop(d)
        data_clean = data
        return data_clean
   
    def time_in_range(self, start, end, xs,xe):
        #Return true if x is in the range [start, end]
        if start <= end:
            return start<= xs and xe <= end
        else:
            
            return start<= xs or xe <= end

    def max_time(self): 

        # Initialize maximum time 
        #print(self.data[0])
        max_time1 = self.data[0]['time']
        for d in self.data:
            if d['time'] > max_time1: 
                #print(type(d['time']))
                max_time1 = d['time']
        return max_time1
        
    def time_slice(self):
        # The Time Span is from days chosen by user to current date time
        # The date-time of encounter + duration should fall in the time slice
        #self.clean_data()
        time_slice_start = self.max_time() - datetime.timedelta(days = int(input("Enter Number of Days of Simulation")))
        #print(time_slice_start)
        time_slice_end = self.max_time()
        #print(time_slice_end)
        timestep = int(input("Enter timestep"))
        
        dfinal=[]
        interactions={}
        cdata = self.data
        while(time_slice_start < time_slice_end):
            dlist=[]
            for d in cdata:
                interactions={}
                time_interact_start = d['time']
                if (d['time'] >= time_slice_start) and (d['time'] < (time_slice_start+datetime.timedelta(hours=timestep))):
                    interactions['lambda']=d['payload']['unobserved'].get('signal_strength')
                    interactions['human_id']=d['human_id']
                    interactions['other_human_id']=d['payload']['unobserved']['human2_id']
                    interactions['human1_isinfected']=d['payload']['unobserved']['human1']['is_infected']
                    interactions['human2_isinfected']=d['payload']['unobserved']['human2']['is_infected']
                    dlist.append(interactions)
            dfinal.append(dlist)  
            time_slice_start+=datetime.timedelta(hours = int(timestep))
#         print(len(dfinal))
#         print(dfinal)        
        return dfinal