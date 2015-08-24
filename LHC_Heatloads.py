import numpy as np
import TimberManager as tm

class Heatload:
    def __init__(self, timber_variable, sector):

        if type(timber_variable) is str:
            dict_timber = tm.parse_timber_file(timber_variable, verbose=True)
            timber_variable_hl = dict_timber[get_variable_dict(sector)['ARC_AVG']]

        elif type(timber_variable) is dict:
            timber_variable_hl = timber_variable[get_variable_dict(sector)['ARC_AVG']]

        # print np.squeeze(np.array(timber_variable_hl.values)).shape
        # print np.squeeze(np.array(timber_variable_hl.values))

        self.t_stamps = np.float_(np.array(timber_variable_hl.t_stamps))
        self.hl = np.squeeze(np.float_(np.array(timber_variable_hl.values)))



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


average_arcs_variable_list = variable_list
variable_lists_heatloads = {}

variable_lists_heatloads['AVG_ARC'] = average_arcs_variable_list()

variable_lists_heatloads['Q4D2s_IR1'] = 'QRLFD_04L1_QBS947.POSST QRLFC_04R1_QBS947.POSST'.split()
variable_lists_heatloads['Q4D2s_IR5'] = 'QRLFC_04L5_QBS947.POSST QRLFD_04R5_QBS947.POSST'.split()
variable_lists_heatloads['Q4D2s_IR2'] = 'QRLFE_04L2_QBS947.POSST QRLFF_04R2_QBS947.POSST'.split()
variable_lists_heatloads['Q4D2s_IR8'] = 'QRLFE_04L8_QBS947.POSST QRLFF_04R8_QBS947.POSST'.split()

variable_lists_heatloads['Q6s_IR1'] = 'QRLEC_06L1_QBS947.POSST QRLEC_06R1_QBS947.POSST'.split()
variable_lists_heatloads['Q6s_IR5'] = 'QRLEC_06L5_QBS947.POSST QRLEC_06R5_QBS947.POSST'.split()
variable_lists_heatloads['Q6s_IR2'] = 'QRLEA_06L2_QBS947.POSST QRLEA_06R2_QBS947.POSST'.split()
variable_lists_heatloads['Q6s_IR8'] = 'QRLEA_06L8_QBS947.POSST QRLDE_06R8_QBS947.POSST'.split()

variable_lists_heatloads['Q5s_IR1'] = 'QRLEC_05L1_QBS947.POSST QRLEC_05R1_QBS947.POSST'.split()
variable_lists_heatloads['Q5s_IR5'] = 'QRLEC_05L5_QBS947.POSST QRLEC_05R5_QBS947.POSST'.split()
variable_lists_heatloads['Q5s_IR2'] = 'QRLEA_05L2_QBS947.POSST QRLEA_05R2_QBS947.POSST'.split()
variable_lists_heatloads['Q5s_IR8'] = 'QRLEA_05L8_QBS947.POSST QRLEA_05R8_QBS947.POSST'.split()

variable_lists_heatloads['IT_IR1'] = 'QRLGA_03L1_QBS947.POSST QRLGC_03R1_QBS947.POSST'.split()
variable_lists_heatloads['IT_IR5'] = 'QRLGD_03L5_QBS947.POSST QRLGB_03R5_QBS947.POSST'.split()
variable_lists_heatloads['IT_IR2'] = 'QRLGF_03L2_QBS947.POSST QRLGE_03R2_QBS947.POSST'.split()
variable_lists_heatloads['IT_IR8'] = 'QRLGF_03L8_QBS947.POSST QRLGE_03R8_QBS947.POSST'.split()

variable_lists_heatloads['special_HC_Q1'] = 'QRLAA_13L5_QBS943_Q1.POSST QRLAA_33L5_QBS947_Q1.POSST QRLAA_13R4_QBS947_Q1.POSST'.split()
variable_lists_heatloads['special_HC_D2'] = 'QRLAA_13L5_QBS943_D2.POSST QRLAA_13R4_QBS947_D2.POSST QRLAA_33L5_QBS947_D2.POSST'.split()
variable_lists_heatloads['special_HC_D3'] = 'QRLAA_13L5_QBS943_D3.POSST QRLAA_13R4_QBS947_D3.POSST QRLAA_33L5_QBS947_D3.POSST'.split()
variable_lists_heatloads['special_HC_D4'] = 'QRLAA_13R4_QBS947_D4.POSST QRLAA_33L5_QBS947_D4.POSST QRLAA_13L5_QBS943_D4.POSST'.split()
variable_lists_heatloads['special_total'] = 'QRLAA_13R4_QBS947.POSST QRLAA_33L5_QBS947.POSST QRLAA_13L5_QBS943.POSST'.split()
