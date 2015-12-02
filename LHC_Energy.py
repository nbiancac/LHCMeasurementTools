import numpy as np
import TimberManager as tm

class energy:
    def __init__(self, timber_variable, beam=0):
        if type(timber_variable) is str:
            if not (beam == 1 or beam == 2):
                raise ValueError('You need to specify which beam! (1 or 2)')
            dict_timber = tm.parse_timber_file(timber_variable, verbose=True)
            timber_variable_energy = dict_timber[get_variable_dict(beam)['ENERGY']]
        elif type(timber_variable) is dict:
            timber_variable_energy = timber_variable[get_variable_dict(beam)['ENERGY']]

        self.t_stamps = timber_variable_energy.t_stamps
        self.energy = np.atleast_1d(np.squeeze(timber_variable_energy.float_values()))
        #self.energy = map(lambda x: float(x[0]), self.energy)
	
        self.t_stamps = np.array(self.t_stamps)
        self.energy = np.array(self.energy)
		
    def nearest_older_sample(self, t_obs):
        ind_min = np.argmin(np.abs(self.t_stamps - t_obs))
        if self.t_stamps[ind_min] > t_obs:
            ind_min -= 1
        return self.energy[ind_min]
	

def get_variable_dict(beam):
    var_dict = {}
    var_dict['ENERGY'] = 'LHC.BSRA.US45.B%d:ABORT_GAP_ENERGY'%beam
    return var_dict

def variable_list(beams = [1,2]):    
    var_list = []
    for beam in beams:
		var_list += get_variable_dict(beam).values()

    return var_list
