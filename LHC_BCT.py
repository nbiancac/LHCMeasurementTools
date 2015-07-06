import numpy as np
import TimberManager as tm

class BCT(object):
    def __init__(self, timber_variable, beam=0):

        if type(timber_variable) is str:
            if not (beam == 1 or beam == 2):
                raise ValueError('You need to specify which beam! (1 or 2)')
            dict_timber = tm.parse_timber_file(timber_variable, verbose=True)
            timber_variable_BCT = dict_timber[get_variable_dict(beam)['BEAM_INTENSITY']]
        elif type(timber_variable) is dict:
            timber_variable_BCT = timber_variable[get_variable_dict(beam)['BEAM_INTENSITY']]            

        self.t_stamps = np.float_(np.array(timber_variable_BCT.t_stamps))
        self.values = np.squeeze(np.float_(np.array(timber_variable_BCT.values)))

    def nearest_older_sample(self, t_obs, flag_return_time=False):
        ind_min = np.argmin(np.abs(self.t_stamps - t_obs))
        if self.t_stamps[ind_min] > t_obs:
            ind_min -= 1
        if flag_return_time:	
            if ind_min == -1:
                return 0.*self.values[ind_min], -1
            else:	
                return self.values[ind_min], self.t_stamps[ind_min]
        else:
            if ind_min == -1:
                return 0.*self.values[ind_min]
            else:	
                return self.values[ind_min]

		
def get_variable_dict(beam):
    var_dict = {}
    var_dict['BEAM_INTENSITY'] = 'LHC.BCTDC.A6R4.B%d:BEAM_INTENSITY'%beam

    return var_dict

def variable_list(beams = [1,2]):
    var_list = []
    for beam in beams:
        var_list += get_variable_dict(beam).values()

    return var_list
