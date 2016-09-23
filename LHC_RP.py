import numpy as np
import datetime
import pytimber 

mdb=pytimber.LoggingDB(source='mdb')

class RP(object):

    def __init__(self, timber_variable, beam=0):

        if type(timber_variable) is dict:
            dict_timber = timber_variable            
        
        self.beam=beam
        self.dictall = dict_timber;
    
    def select_coll(self,namecoll):
        self.t_stamps=self.dictall[namecoll][0]
        self.t_str=[datetime.datetime.fromtimestamp(self.t_stamps[ii]) for ii in np.arange(len(self.t_stamps))]
        self.values=self.dictall[namecoll][1]
        
    def interp_with(self, obj):
        
        
        old_t_stamps=self.t_stamps
        new_t_stamps=obj.t_stamps
    
        for el in vars(self):
    
            if type(getattr(self,el)) in [np.ndarray]:
                
                new_values=np.interp(new_t_stamps,old_t_stamps, getattr(self,el))
                np.shape(new_values)
                setattr(self,el,new_values)
        
        self.t_str=[datetime.datetime.fromtimestamp(self.t_stamps[ii]) for ii in np.arange(len(self.t_stamps))]

def variable_list(beam =1):
    
    var_list = mdb.search('XRP%B'+str(beam)+'%LVDT%LU')
           
    return var_list
