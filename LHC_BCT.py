import numpy as np
import pytimber
import datetime
import matplotlib as plt

class BCT(object):
    def __init__(self, timber_variable, beam=0):

        if type(timber_variable) is dict:
            timber_variable_BCT = timber_variable[get_variable_dict(beam)['BEAM_INTENSITY']]           
        
        self.beam=beam
        self.t_stamps = np.float_(np.array(timber_variable_BCT[0]))
        self.t_str=[datetime.datetime.fromtimestamp(self.t_stamps[ii]) for ii in np.arange(len(self.t_stamps))]
        self.values = np.squeeze(np.float_(np.array(timber_variable_BCT[1])))

    def plot(self):
        plt.plot(self.t_stamps,self.values)

    
    def interp_with(self, obj):
        
        old_t_stamps=self.t_stamps
        new_t_stamps=np.sort(np.unique(np.append(old_t_stamps,obj.t_stamps)))
        
        for el in vars(self):
    
            if type(getattr(self,el)) in [np.ndarray]:
                
                if len(np.shape(getattr(self,el)))==1 & (len(getattr(self,el))>0):
                
                    new_values=np.interp(new_t_stamps,old_t_stamps, getattr(self,el))

                    setattr(self,el,new_values)
        
        self.t_str=[datetime.datetime.fromtimestamp(self.t_stamps[ii]) for ii in np.arange(len(self.t_stamps))]
        
def get_variable_dict(beam):
    var_dict = {}
    var_dict['BEAM_INTENSITY'] = 'LHC.BCTDC.A6R4.B%d:BEAM_INTENSITY'%beam

    return var_dict

def variable_list(beams = [1,2]):
    var_list = []
    for beam in beams:
        var_list += get_variable_dict(beam).values()

    return var_list