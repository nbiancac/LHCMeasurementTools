import numpy as np
import pytimber
import datetime

class BBQ(object):

    def __init__(self, timber_variable_bbq, beam=0):

        if not (beam == 1 or beam == 2):
            raise ValueError('You need to specify which beam! (1 or 2)')
        

        if type(timber_variable_bbq) is dict:
            dict_timber = timber_variable_bbq
        
        self.beam = beam
        
        self.amp_1 = np.squeeze(np.array(
            dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_AMPL_1'.format(beam)][1]))
        self.amp_2  = np.squeeze(np.array(
            dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_AMPL_2'.format(beam)][1]))
        
        self.xamp_1 = np.squeeze(np.array(
            dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_X_AMPL_1'.format(beam)][1]))
        self.xamp_2 = np.squeeze(np.array(
            dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_X_AMPL_2'.format(beam)][1]))
        
        self.qh  = dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:TUNE_H'.format(beam)][1]
        self.qv  = dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:TUNE_V'.format(beam)][1]
        
        self.q1  = dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_FREQ_1'.format(beam)][1]
        self.q2  = dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_FREQ_2'.format(beam)][1]
        
        self.t_stamps = np.ravel(np.squeeze(np.array(
            dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_AMPL_1'.format(beam)][0])))
        
        self.t_str=[datetime.datetime.fromtimestamp(self.t_stamps[ii]) for ii in np.arange(len(self.t_stamps))]
    
        
    def interp_with(self, obj):
        
        old_t_stamps=self.t_stamps
        new_t_stamps=np.sort(np.unique(np.append(old_t_stamps,obj.t_stamps)))
        
        for el in vars(self):
    
            if type(getattr(self,el)) in [np.ndarray]:
                
                new_values=np.interp(new_t_stamps,old_t_stamps, getattr(self,el))
                np.shape(new_values)
                setattr(self,el,new_values)
        
        self.t_str=[datetime.datetime.fromtimestamp(self.t_stamps[ii]) for ii in np.arange(len(self.t_stamps))]

        

class BBQ_FFT(object):

    def __init__(self, timber_variable_bbq, beam=0):

        if not (beam == 1 or beam == 2):
            raise ValueError('You need to specify which beam! (1 or 2)')
        
        if type(timber_variable_bbq) is dict:
            dict_timber = timber_variable_bbq

        self.beam = beam

        self.fft_h  = dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:FFT_DATA_H'.format(beam)][1]
        self.fft_v  = dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:FFT_DATA_V'.format(beam)][1]
        
        self.t_stamps = np.ravel(np.squeeze(np.array(dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_FREQ_1'.format(beam)][0])))
        self.t_str=[datetime.datetime.fromtimestamp(self.t_stamps[ii]) for ii in np.arange(len(self.t_stamps))]
        
class BBQ_RAW(object):

    def __init__(self, timber_variable_bbq, beam=0):

        if not (beam == 1 or beam == 2):
            raise ValueError('You need to specify which beam! (1 or 2)')
        

        if type(timber_variable_bbq) is dict:
            dict_timber = timber_variable_bbq
        
        self.beam = beam
        
        self.gated_h  = dict_timber['LHC.BQBBQ.CONTINUOUS.B{:d}:ACQ_DATA_H'.format(beam)][1]
        self.gated_v  = dict_timber['LHC.BQBBQ.CONTINUOUS.B{:d}:ACQ_DATA_V'.format(beam)][1]
        
        self.HS_h  = dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:ACQ_DATA_H'.format(beam)][1]
        self.HS_v  = dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:ACQ_DATA_V'.format(beam)][1]
        
        self.amph = np.array([]);
        self.ampv = np.array([]);
        
        self.qh = np.array([]);
        self.qv = np.array([]);
        
        self.t_stamps = np.ravel(np.squeeze(np.array(dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:ACQ_DATA_H'.format(beam)][0])))
        self.t_str=[datetime.datetime.fromtimestamp(self.t_stamps[ii]) for ii in np.arange(len(self.t_stamps))]
        
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
    var_dict['BBQ_HS_AMPL_1'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_AMPL_1'.format(beam)
    var_dict['BBQ_HS_AMPL_2'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_AMPL_2'.format(beam)
    var_dict['BBQ_HS_Q_1'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_FREQ_1'.format(beam)
    var_dict['BBQ_HS_Q_2'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_FREQ_2'.format(beam)
    var_dict['BBQ_HS_TUNE_H'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:TUNE_H'.format(beam)
    var_dict['BBQ_HS_TUNE_V'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:TUNE_V'.format(beam)
    var_dict['BBQ_HS_WIDTH_1'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_WIDTH_1'.format(beam)
    var_dict['BBQ_HS_WIDTH_2'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_WIDTH_2'.format(beam)
    var_dict['BBQ_HS_X_AMPL_1'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_X_AMPL_1'.format(beam)
    var_dict['BBQ_HS_X_AMPL_2'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_X_AMPL_2'.format(beam)
    var_dict['BBQ_HS_FFT_H'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:FFT_DATA_H'.format(beam)
    var_dict['BBQ_HS_FFT_V'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:FFT_DATA_V'.format(beam)
    

    return var_dict


def variable_list(beams = [1, 2]):
    var_list = []
    for beam in beams:
        var_list += get_variable_dict(beam).values()

    return var_list

def variable_list_RAW(beams = [1,2]):
	
    var_list = []
    for beam in beams:
        var_list+=['LHC.BQBBQ.CONTINUOUS.B%d:ACQ_DATA_H'%beam,
        'LHC.BQBBQ.CONTINUOUS.B%d:ACQ_DATA_V'%beam,
        'LHC.BQBBQ.CONTINUOUS_HS.B%d:ACQ_DATA_H'%beam,
        'LHC.BQBBQ.CONTINUOUS_HS.B%d:ACQ_DATA_V'%beam]
	return var_list