import numpy as np
import TimberManager as tm

class Heatload:
    def __init__(self, timber_variable, sector):

        if type(timber_variable) is str:
            dict_timber = tm.parse_timber_file(timber_variable, verbose=True)
            timber_variable_hl = dict_timber[get_variable_dict(sector)['ARC_AVG']]

        elif type(timber_variable) is dict:
            timber_variable_hl = timber_variable[get_variable_dict(sector)['ARC_AVG']]

        self.t_stamps = np.float_(np.array(timber_variable_hl.t_stamps))
        self.hl = np.float_(np.array(timber_variable_hl.values).flatten())


def get_variable_dict(sector):
    var_dict = {}
    var_dict['ARC_AVG'] = 'S%d_QBS_AVG_ARC.POSST'%sector

    return var_dict

def variable_list(sectors=[12,23,34,45,56,67,78,81]):
    var_list = []
    for sector in sectors:
        var_list += get_variable_dict(sector).values()

    return var_list

def sector_list():
    sector_list = [12,23,34,45,56,67,78,81]

    return sector_list
