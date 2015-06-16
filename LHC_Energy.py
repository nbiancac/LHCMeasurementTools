import numpy as np
import TimberManager as tm

class energy:
    def __init__(self, timber_variable_energy, beam=0):
        if type(timber_variable_energy) is str:
            if not (beam == 1 or beam == 2):
                raise ValueError('You need to specify which beam! (1 or 2)')
            dict_timber = tm.parse_timber_file(timber_variable_energy, verbose=True)
            timber_variable_energy = dict_timber[get_variable_dict(beam)['ENERGY']]

        self.tstamps = timber_variable_energy.t_stamps
        self.energy = timber_variable_energy.values
		
        self.energy = map(lambda x: float(x[0]), self.energy)
	
        self.tstamps=np.array(self.tstamps)
        self.energy=np.array(self.energy)
		
    def nearest_older_sample(self, t_obs):
        ind_min = np.argmin(np.abs(self.tstamps - t_obs))
        if self.tstamps[ind_min] > t_obs:
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
