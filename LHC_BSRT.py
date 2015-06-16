import numpy as np
import TimberManager as tm

class BSRT:
    def __init__(self, timber_variable_bsrt, beam=0):

        # assume timber_variable_bsrt is filename string for now
        if not (beam == 1 or beam == 2):
            raise ValueError('You need to specify which beam! (1 or 2)')
        dict_timber = tm.parse_timber_file(timber_variable_bsrt, verbose=True)

        sigma_h = dict_timber[get_variable_dict(beam)['SIGMA_H']]
        sigma_v = dict_timber[get_variable_dict(beam)['SIGMA_V']]
        gate = dict_timber[get_variable_dict(beam)['GATE_DELAY']]

        if (sigma_h.t_stamps != sigma_v.t_stamps):
            raise Warning('Timestamps for the two channels (H and V) not equal!')
        if (sigma_v.t_stamps != gate.t_stamps):
            bunches_effectively_recorded = get_bunches_effectively_recorded(gate, sigma_v)             
        else:
            bunches_effectively_recorded = gate 

        t_stamp_list = []
        bunch_n_list = []
        sigma_h_list = []
        sigma_v_list = []

        for ii in xrange(len(bunches_effectively_recorded.t_stamps)):
            if np.mod(ii,10000) == 0:
		print 'expanding %.1f'%(float(ii)/len(bunches_effectively_recorded.t_stamps)*100)+"""%"""	
	
            N_meas = len(bunches_effectively_recorded.values[ii])
            for jj in xrange(N_meas):
		bunch_n_list.append(np.float_(bunches_effectively_recorded.values[ii][jj]))
		sigma_h_list.append(sigma_h.values[ii][jj])
		sigma_v_list.append(sigma_v.values[ii][jj])
		t_stamp_list.append(sigma_v.t_stamps[ii] + float(jj)*1e-3/float(N_meas))        
             
        self.t_stamps = np.array(t_stamp_list)
        self.bunch_n = np.array(bunch_n_list)
        self.sigma_h = np.array(sigma_h_list)
        self.sigma_v = np.array(sigma_v_list)


        def get_bunches_effectively_recorded(gate_timber, sigma_timber):
            recorded_bunches = tm.timber_variable_list()
            i1 = 0
            for i2 in xrange(len(gate_timber.t_stamps)):
                if np.mod(i2,10000) == 0:
                    print 'Cleaning %.1f'%(float(i2)/len(gate_timber.t_stamps)*100)+"""%"""
                if gate_timber.t_stamps[i2] == sigma_timber.t_stamps[i1]:
                    recorded_bunches.t_stamps.append(gate_timber.t_stamps[i2])
                    recorded_bunches.values.append(gate_timber.values[i2])
                    i1 += 1
         
            return recorded_bunches



def get_variable_dict(beam):
    beam_device_list = ['R','L']
    var_dict = {}
    var_dict['GATE_DELAY'] = 'LHC.BSRT.5%s4.B%d:GATE_DELAY'%(beam_device_list[beam-1],beam)
    var_dict['SIGMA_H'] = 'LHC.BSRT.5%s4.B%d:FIT_SIGMA_H'%(beam_device_list[beam-1],beam)
    var_dict['SIGMA_V'] = 'LHC.BSRT.5%s4.B%d:FIT_SIGMA_V'%(beam_device_list[beam-1],beam)

    return var_dict


def variable_list(beams = [1,2]):
    var_list = []
    for beam in beams:
		var_list += get_variable_dict(beam).values()

    return var_list
