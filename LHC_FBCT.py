import numpy as np
import TimberManager as tm

class FBCT:
    def __init__(self, timber_variable_FBCT, beam=0):

        if type(timber_variable_FBCT) is str:
            if not (beam == 1 or beam == 2):
                raise ValueError('You need to specify which beam! (1 or 2)')
            dict_timber = tm.parse_timber_file(timber_variable_FBCT, verbose=True)
            timber_variable_FBCT = dict_timber[get_variable_dict(beam)['BUNCH_INTENSITY']]

        self.tstamps = timber_variable_FBCT.t_stamps
        self.bint = timber_variable_FBCT.values
        self.bint = map(lambda x: np.array(map(float, x)), self.bint)

        self.tstamps = np.array(self.tstamps)
        self.totint = np.array(map(sum, self.bint))
		

    def nearest_older_sample(self, t_obs, flag_return_time=False):
        ind_min = np.argmin(np.abs(self.tstamps - t_obs))
        if self.tstamps[ind_min] > t_obs:
            ind_min -= 1
        if flag_return_time:	
            if ind_min == -1:
                return 0.*self.bint[ind_min], -1
            else:	
                return self.bint[ind_min], self.tstamps[ind_min]
        else:
            if ind_min == -1:
                return 0.*self.bint[ind_min]
            else:	
                return self.bint[ind_min]

		
def get_variable_dict(beam):
    var_dict = {}
    var_dict['BUNCH_INTENSITY'] = 'LHC.BCTFR.A6R4.B%d:BUNCH_INTENSITY'%beam
    return var_dict

def variable_list(beams = [1,2]):
    
    var_list = []
    for beam in beams:
		var_list += get_variable_dict(beam).values()
		
    return var_list
