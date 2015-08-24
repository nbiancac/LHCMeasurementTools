# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import TimberManager as tm
import numpy as np

class Phase:
    def __init__(self, timber_variable):

        if type(timber_variable) is str:
            dict_timber = parse_csv_file(timber_variable) 

        elif type(timber_variable) is dict:
            dict_timber = timber_variable

        timber_variable_phase = dict_timber['PHASE'] 
        timber_variable_bunches = dict_timber['BUNCHES']
        
        self.t_stamps = np.float_(np.array(timber_variable_phase.t_stamps)) 
        values_raw = np.float_(np.array(timber_variable_phase.values)) 
        bunches_raw = np.float_(np.array(timber_variable_bunches.values)) 

        # create variables with all bunch slots
        nslots = 3564
        self.bunches = np.arange(nslots)
        self.values = np.zeros((len(self.t_stamps), nslots))
        for ii in xrange(len(bunches_raw)):
            bunch = bunches_raw[ii]
            self.values[:,bunch-1] = values_raw[:,ii] 

    def stick_power_loss(self, fbct_obj, V_rf=6e6, bct_obj=None):
        qe = 1.602176565e-19
        T_rev = 88.9e-6 
        energy_loss_part = -V_rf * np.sin(self.values*np.pi/180.)
        energy_loss_bunch = 0*energy_loss_part
        n_traces = len(self.t_stamps)
        for ii in xrange(n_traces):
            fbct_raw, t_fbct_curr = fbct_obj.nearest_older_sample(self.t_stamps[ii], flag_return_time=True)
            if bct_obj is not None:
                bct_curr = bct_obj.nearest_older_sample(t_fbct_curr)
                fbct_curr = fbct_raw/np.float_(np.sum(fbct_raw))*bct_curr
            else:
                fbct_curr = fbct_raw

            energy_loss_bunch[ii,:] = energy_loss_part[ii,:] * fbct_curr 
        
        self.power_loss = energy_loss_bunch*qe/T_rev

    def nearest_older_sample_power_loss(self, t_obs, flag_return_time=False):
        ind_min = np.argmin(np.abs(self.t_stamps - t_obs))
        if self.t_stamps[ind_min] > t_obs:
            ind_min -= 1
        if flag_return_time:	
            if ind_min == -1:
                return 0.*self.power_loss[ind_min], -1
            else:	
                return self.power_loss[ind_min], self.t_stamps[ind_min]
        else:
            if ind_min == -1:
                return 0.*self.power_loss[ind_min]
            else:	
                return self.power_loss[ind_min]


def parse_csv_file(filename):

    with open(filename) as fid:
        csv_lines = fid.readlines() 

    bunches = tm.timber_variable_list()
    phase = tm.timber_variable_list()

    N_lines = len(csv_lines)
    i_ln = 1

    line = csv_lines[i_ln]
    line = line.split('\r\n')[0]
    bunch_list = line[1:].split(',')
    bunches.values = bunch_list
    i_ln += 1

    while i_ln < N_lines:
        line = csv_lines[i_ln]
        line = line.split('\r\n')[0]
        line_obj = csv_data_line(line)
        (phase.t_stamps).append(line_obj.timestamp) 
        (phase.values).append(line_obj.data_strings)
        i_ln += 1

    variables = {}
    variables['PHASE'] = phase
    variables['BUNCHES'] = bunches

    return variables


class csv_data_line():
    def __init__(self, rline):
        list_values = rline.split(',')
        t_string = list_values[0]
        self.timestamp = tm.timb_timestamp2float(t_string.split('.')[0])
        self.data_strings = list_values[1:]
		
