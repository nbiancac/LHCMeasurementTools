import numpy as np
import TimberManager as tm

class Pressure(object):
    def __init__(self, timber_variable, press_gauge):
        if type(timber_variable) is str:
            dict_timber = tm.parse_timber_file(timber_variable, verbose=True)
            timber_press_gauge = dict_timber[press_gauge]
        elif type(timber_variable) is dict:
            timber_press_gauge = timber_variable[press_gauge]

        self.t_stamps = np.array(timber_press_gauge.t_stamps)
        self.values = np.float_(np.array(timber_press_gauge.values).flatten())

def get_variable_dict(gauge_group):
    var_dict = {}

    # MKI pressure gauges.
    var_dict['MKI'] = [
		'VGPB.14.5R8.R.PR', 'VGPB.59.5R8.R.PR', 'VGPB.98.5R8.R.PR',
		'VGPB.138.5R8.R.PR', 'VGPB.176.5R8.R.PR', 'MKI.A5L2.B1:PRESSURE',
		'MKI.B5L2.B1:PRESSURE', 'MKI.C5L2.B1:PRESSURE', 'MKI.D5L2.B1:PRESSURE',
		'VGPB.14.5L2.B.PR', 'VGPB.59.5L2.B.PR', 'VGPB.98.5L2.B.PR',
		'VGPB.138.5L2.B.PR', 'VGPB.176.5L2.B.PR', 'MKI.A5R8.B2:PRESSURE',
		'MKI.B5R8.B2:PRESSURE', 'MKI.C5R8.B2:PRESSURE', 'MKI.D5R8.B2:PRESSURE' ]

    return var_dict[gauge_group]

def variable_list(gauge_group):
	var_list = get_variable_dict(gauge_group)
	return var_list
