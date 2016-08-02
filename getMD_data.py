#!/home/nbiancac/anaconda2/bin/python
# coding: utf-8

# ## Load fill and beam modes

# In[1]:

import pytimber
import datetime
import pickle
import pagestore
import time, calendar
import os
import numpy as np


filln=5130

mdb=pytimber.LoggingDB(source='mdb')
db=pagestore.PageStore('/home/nbiancac/HDD/Work/MD/LHC/DB/lhc.db','/home/nbiancac/HDD/Work/MD/LHC/DB/')    

beamMode1 = 'RAMP'
beamMode2 = 'BEAMDUMP'

a =mdb.getLHCFillData(fill_number=filln)['beamModes']
for ind,el in enumerate(a):
    if el['mode'] == beamMode1:
        ts1=mdb.getLHCFillData(fill_number=filln)['beamModes'][ind]['startTime']
        print beamMode1+' startTime: %.1f'%ts1
        
for ind,el in enumerate(a):
    if el['mode'] == beamMode2:
        ts2=mdb.getLHCFillData(fill_number=filln)['beamModes'][ind]['startTime']
        print beamMode2+' startTime: %.1f'%ts2
# ts1 = time.time()-1*3600
# ts2 = time.time()

# ts1 = calendar.timegm(time.strptime("2016-07-29 04:00:00","%Y-%m-%d %H:%M:%S"))-2*3600
# ts2 = calendar.timegm(time.strptime("2016-07-29 07:00:00","%Y-%m-%d %H:%M:%S"))-2*3600

print 'ts1 = '+time.strftime("%b %d %Y %H:%M:%S", time.localtime(ts1))
print 'ts2 = '+time.strftime("%b %d %Y %H:%M:%S", time.localtime(ts2))

# segment BBQ every 5 minutes
Nsegments = np.floor(ts2-ts1)/(60) 
print 'Segmenting BBQ data in 1 minute: %d files'%Nsegments


# ### Getting data from Timber and stored in Pagestore

# BCT
import LHC_BCT
data=mdb.get(LHC_BCT.variable_list(beams=[1,2]),ts1,ts2)
db.store(data)


# BBQ
#import LHC_BBQ
#times=np.linspace(ts1,ts2,Nsegments)
#for ii in np.arange(1,len(times)-1):
#    data=mdb.get(LHC_BBQ.variable_list(beams=[1,2]),ts1,ts2)
#    db.store(data)

# BBQ RAW
import LHC_BBQ
times=np.linspace(ts1,ts2,Nsegments)
for ii in np.arange(len(times)-1):
    print '%d/%d'%(ii,len(times)-2)
    data=mdb.get(LHC_BBQ.variable_list_RAW(beams=[1,2]),times[ii],times[ii+1])
    db.store(data)
    
# BSRT
import LHC_BSRT
times=np.linspace(ts1,ts2,2*Nsegments)
for ii in np.arange(len(times)-1):
	print '%d/%d'%(ii,len(times)-2)
	data=mdb.get(LHC_BSRT.variable_list(beams=[1,2]),times[ii],times[ii+1])
	db.store(data)


# BQM
import LHC_BQM
times=np.linspace(ts1,ts2,2*Nsegments)
for ii in np.arange(len(times)-1):
	data=mdb.get(LHC_BQM.variable_list(beams=[1,2]),ts1,ts2)
	db.store(data)


# FBCT
import LHC_FBCT
times=np.linspace(ts1,ts2,Nsegments)
for ii in np.arange(len(times)-1):
    data=mdb.get(LHC_FBCT.variable_list(beams=[1,2]),times[ii],times[ii+1])
    db.store(data)


# Energy
import LHC_Energy
data=mdb.get(LHC_Energy.variable_list(beams=[1,2]),ts1,ts2)
db.store(data)



# Collimators
import LHC_Coll
data=mdb.get(LHC_Coll.variable_list(beam=1),ts1,ts2)
db.store(data)
data=mdb.get(LHC_Coll.variable_list(beam=2),ts1,ts2)
db.store(data)

