import numpy as np
import datetime

class Coll(object):

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
    var_list = []
    if beam==1:
        var_list=[
        'TCDQA.A4R6.B1:MEAS_LVDT_LD',
        'TCL.4R1.B1:MEAS_LVDT_GU',
        'TCL.4R5.B1:MEAS_LVDT_GU',
        'TCL.5R1.B1:MEAS_LVDT_GU',
        'TCL.5R5.B1:MEAS_LVDT_GU',
        'TCL.6R1.B1:MEAS_LVDT_GU',
        'TCL.6R5.B1:MEAS_LVDT_GU',
        'TCLA.6R3.B1:MEAS_LVDT_GU',
        'TCLA.7R3.B1:MEAS_LVDT_GU',
        'TCLA.A5R3.B1:MEAS_LVDT_GU',
        'TCLA.A6R7.B1:MEAS_LVDT_GU',
        'TCLA.A7R7.B1:MEAS_LVDT_GU',
        'TCLA.B5R3.B1:MEAS_LVDT_GU',
        'TCLA.B6R7.B1:MEAS_LVDT_GU',
        'TCLA.C6R7.B1:MEAS_LVDT_GU',
        'TCLA.D6R7.B1:MEAS_LVDT_GU',
        'TCLIA.4R2:MEAS_LVDT_GU',
        'TCLIB.6R2.B1:MEAS_LVDT_GU',
        'TCP.6L3.B1:MEAS_LVDT_GU',
        'TCP.B6L7.B1:MEAS_LVDT_GU',
        'TCP.C6L7.B1:MEAS_LVDT_GU',
        'TCP.D6L7.B1:MEAS_LVDT_GU',
        'TCSG.4R3.B1:MEAS_LVDT_GU',
        'TCSG.5L3.B1:MEAS_LVDT_GU',
        'TCSG.6R7.B1:MEAS_LVDT_GU',
        'TCSG.A4L7.B1:MEAS_LVDT_GU',
        'TCSG.A4R7.B1:MEAS_LVDT_GU',
        'TCSG.A5L7.B1:MEAS_LVDT_GU',
        'TCSG.A5R3.B1:MEAS_LVDT_GU',
        'TCSG.A6L7.B1:MEAS_LVDT_GU',
        'TCSG.B4L7.B1:MEAS_LVDT_GU',
        'TCSG.B5L7.B1:MEAS_LVDT_GU',
        'TCSG.B5R3.B1:MEAS_LVDT_GU',
        'TCSG.B5R7.B1:MEAS_LVDT_GU',
        'TCSG.D4L7.B1:MEAS_LVDT_GU',
        'TCSG.D5R7.B1:MEAS_LVDT_GU',
        'TCSG.E5R7.B1:MEAS_LVDT_GU',
        'TCSP.A4R6.B1:MEAS_LVDT_GU',
        'TCTPH.4L1.B1:MEAS_LVDT_GU',
        'TCTPH.4L2.B1:MEAS_LVDT_GU',
        'TCTPH.4L5.B1:MEAS_LVDT_GU',
        'TCTPH.4L8.B1:MEAS_LVDT_GU',
        'TCTPV.4L1.B1:MEAS_LVDT_GU',
        'TCTPV.4L2.B1:MEAS_LVDT_GU',
        'TCTPV.4L5.B1:MEAS_LVDT_GU',
        'TCTPV.4L8.B1:MEAS_LVDT_GU',
        'TDI.4L2:MEAS_LVDT_GU'];

    elif beam==2:
        var_list=[
        'TCDQA.A4L6.B2:MEAS_LVDT_LD',
        'TCL.4L1.B2:MEAS_LVDT_GU',
        'TCL.4L5.B2:MEAS_LVDT_GU',
        'TCL.5L1.B2:MEAS_LVDT_GU',
        'TCL.5L5.B2:MEAS_LVDT_GU',
        'TCL.6L1.B2:MEAS_LVDT_GU',
        'TCL.6L5.B2:MEAS_LVDT_GU',
        'TCLA.6L3.B2:MEAS_LVDT_GU',
        'TCLA.7L3.B2:MEAS_LVDT_GU',
        'TCLA.A5L3.B2:MEAS_LVDT_GU',
        'TCLA.A6L7.B2:MEAS_LVDT_GU',
        'TCLA.A7L7.B2:MEAS_LVDT_GU',
        'TCLA.B5L3.B2:MEAS_LVDT_GU',
        'TCLA.B6L7.B2:MEAS_LVDT_GU',
        'TCLA.C6L7.B2:MEAS_LVDT_GU',
        'TCLA.D6L7.B2:MEAS_LVDT_GU',
        'TCLIA.4L8:MEAS_LVDT_GU',
        'TCLIB.6L8.B2:MEAS_LVDT_GU',
        'TCP.6R3.B2:MEAS_LVDT_GU',
        'TCP.B6R7.B2:MEAS_LVDT_GU',
        'TCP.C6R7.B2:MEAS_LVDT_GU',
        'TCP.D6R7.B2:MEAS_LVDT_GU',
        'TCSG.4L3.B2:MEAS_LVDT_GU',
        'TCSG.5R3.B2:MEAS_LVDT_GU',
        'TCSG.6L7.B2:MEAS_LVDT_GU',
        'TCSG.A4L7.B2:MEAS_LVDT_GU',
        'TCSG.A4R7.B2:MEAS_LVDT_GU',
        'TCSG.A5L3.B2:MEAS_LVDT_GU',
        'TCSG.A5R7.B2:MEAS_LVDT_GU',
        'TCSG.A6R7.B2:MEAS_LVDT_GU',
        'TCSG.B4R7.B2:MEAS_LVDT_GU',
        'TCSG.B5L3.B2:MEAS_LVDT_GU',
        'TCSG.B5L7.B2:MEAS_LVDT_GU',
        'TCSG.B5R7.B2:MEAS_LVDT_GU',
        'TCSG.D4R7.B2:MEAS_LVDT_GU',
        'TCSG.D5L7.B2:MEAS_LVDT_GU',
        'TCSG.E5L7.B2:MEAS_LVDT_GU',
        'TCSP.A4L6.B2:MEAS_LVDT_GU',
        'TCTPH.4R1.B2:MEAS_LVDT_GU',
        'TCTPH.4R2.B2:MEAS_LVDT_GU',
        'TCTPH.4R5.B2:MEAS_LVDT_GU',
        'TCTPH.4R8.B2:MEAS_LVDT_GU',
        'TCTPV.4R1.B2:MEAS_LVDT_GU',
        'TCTPV.4R2.B2:MEAS_LVDT_GU',
        'TCTPV.4R5.B2:MEAS_LVDT_GU',
        'TCTPV.4R8.B2:MEAS_LVDT_GU',
        'TDI.4R8:MEAS_LVDT_GU'];
            
            
    return var_list