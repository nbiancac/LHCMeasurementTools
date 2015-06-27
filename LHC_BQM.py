import numpy as np
import TimberManager as tm

class filled_buckets:
    def __init__(self, timber_variable, beam=0):

        if type(timber_variable) is str:
            if not (beam == 1 or beam == 2):
                raise ValueError('You need to specify which beam! (1 or 2)')
            dict_timber = tm.parse_timber_file(timber_variable, verbose=True)
            timber_variable_filled = dict_timber[get_variable_dict(beam)['FILLED_BUCKETS']]
        elif type(timber_variable) is dict:
            timber_variable_filled = timber_variable[get_variable_dict(beam)['FILLED_BUCKETS']]            
        self.t_stamps = np.array(timber_variable_filled.t_stamps)
        self.fillbuck = timber_variable_filled.values		
        self.fillbuck = map(lambda x: np.array(map(lambda y: int(float(y)), x)), self.fillbuck)
        self.fillbuck = map(lambda x: (x-1)/10, self.fillbuck)
        self.fillbuck = map(lambda x: x[x>=0], self.fillbuck)

        self.Nbun = map(len, self.fillbuck)
        N_acq = len(self.Nbun)
            
        self.flag_filled = []
        for ii in xrange(N_acq):
            self.flag_filled.append(np.array(map(lambda x: x in self.fillbuck[ii], range(3564))))
			
		
    def nearest_older_sample(self, t_obs):
        ind_min = np.argmin(np.abs(self.t_stamps - t_obs))
        if self.t_stamps[ind_min] > t_obs:
            ind_min -= 1
		
        if ind_min == -1:
            return 0.*self.fillbuck[ind_min]
        else:	
            return self.fillbuck[ind_min]
			
    def nearest_older_sample_flag_filled_Nbun(self, t_obs):
        ind_min = np.argmin(np.abs(self.t_stamps - t_obs))
        if self.t_stamps[ind_min] > t_obs:
            ind_min -= 1 

        if ind_min == -1:
            return [], 0
        else:	
            return self.flag_filled[ind_min], self.Nbun[ind_min]


		
class blength:
    def __init__(self,timber_variable_blength, timber_variable_filled_bucket=None, beam=0):
        
        if type(timber_variable_blength) is str:
            if not (beam == 1 or beam == 2):
                raise ValueError('You need to specify which beam! (1 or 2)')
            dict_timber = tm.parse_timber_file(timber_variable_blength, verbose=True)
            timber_variable_blength = dict_timber[get_variable_dict(beam)['BUNCH_LENGTH']]
            if timber_variable_filled_bucket == None:
                timber_variable_filled_bucket = dict_timber[get_variable_dict(beam)['FILLED_BUCKETS']]

        elif type(timber_variable_blength) is dict:
            dict_timber = timber_variable_blength
            timber_variable_blength = dict_timber[get_variable_dict(beam)['BUNCH_LENGTH']]
            if timber_variable_filled_bucket == None:
                timber_variable_filled_bucket = dict_timber[get_variable_dict(beam)['FILLED_BUCKETS']]


        if isinstance(timber_variable_filled_bucket,tm.timber_variable_list):
            fillbuck_obj = filled_buckets(timber_variable_filled_bucket)
        elif type(timber_variable_filled_bucket) is str:
            if not (beam == 1 or beam == 2):
                raise ValueError('You need to specify which beam! (1 or 2)')
            dict_timber = tm.parse_timber_file(timber_variable_filled_bucket, verbose=True)
            timber_variable_filled_bucket = dict_timber[get_variable_dict(beam)['FILLED_BUCKETS']]
            fillbuck_obj = filled_buckets(timber_variable_filled_bucket)
        elif isinstance(timber_variable_filled_bucket, filled_buckets):
            fillbuck_obj = timber_variable_filled_bucket 
        elif timber_variable_filled_bucket == None:
            raise TypeError('You need to provide a filled_bucket file or object!')
		
        self.t_stamps = timber_variable_blength.t_stamps
        self.blen = []
        blen_timberstyle = timber_variable_blength.values
        blen_timberstyle = map(lambda x: np.array(map(float, x)), blen_timberstyle)
	
        N_acq = len(self.t_stamps)
        
        for ii in xrange(N_acq):
            blen_vect = np.zeros(3564) 
            flag_filled_curr, Nbun_curr = fillbuck_obj.nearest_older_sample_flag_filled_Nbun(self.t_stamps[ii])
            blen_vect[flag_filled_curr] = (blen_timberstyle[ii][:Nbun_curr])
            self.blen.append(blen_vect)
			
        self.t_stamps = np.array(self.t_stamps)
        self.avblen = np.array(map(mean_nonzero, self.blen))


    def nearest_older_sample(self, t_obs, flag_return_time=False):
        ind_min = np.argmin(np.abs(self.t_stamps - t_obs))
        if self.t_stamps[ind_min]>t_obs:
            ind_min -= 1
	
        if flag_return_time:	
            if ind_min == -1:
                return 0.*self.blen[ind_min], -1
            else:	
                return self.blen[ind_min], self.t_stamps[ind_min]
        else:
            if ind_min == -1:
                return 0.*self.blen[ind_min]
            else:	
                return self.blen[ind_min]


def mean_nonzero(x):
    mask_nonzero = x > 0
    if np.sum(mask_nonzero) > 0:
        return np.mean(x[mask_nonzero])
    else:		
        return 0.


def get_variable_dict(beam):
    var_dict = {}
    var_dict['FILLED_BUCKETS'] = 'LHC.BQM.B%d:FILLED_BUCKETS'%beam
    var_dict['BUNCH_LENGTH'] = 'LHC.BQM.B%d:BUNCH_LENGTHS'%beam

    return var_dict


def variable_list(beams = [1,2]):
    var_list = []
    for beam in beams:
		var_list += get_variable_dict(beam).values()

    return var_list
