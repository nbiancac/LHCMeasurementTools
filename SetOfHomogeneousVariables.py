import numpy as np
import TimberManager as tm

class SetOfHomogeneousNumericVariables:
    def __init__(self, variable_list, timber_variables):

        self.variable_list = variable_list

        if type(timber_variables) is str:
            dict_timber = tm.parse_timber_file(timber_variables, verbose=True)
        elif type(timber_variables) is dict:
            dict_timber = timber_variables

        self.timber_variables = {}
        for var_name in self.variable_list:
             self.timber_variables[var_name] = dict_timber[var_name]
             self.timber_variables[var_name].t_stamps = np.float_(np.array(self.timber_variables[var_name].t_stamps))
             self.timber_variables[var_name].values = np.float_(np.squeeze(np.array(self.timber_variables[var_name].values)))

    def aligned(self):
        aligned_list = []
        t_first = self.timber_variables[self.variable_list[0]].t_stamps
        for ii,kk in enumerate(self.variable_list):
            aligned_list.append(np.interp(t_first, self.timber_variables[kk].t_stamps, self.timber_variables[kk].values))
        return t_first, np.array(aligned_list)

    def mean(self):
        t_first, aligned = self.aligned()
        return t_first, np.mean(aligned, axis=0)

    def std(self):
        t_first, aligned = self.aligned()
        return t_first, np.std(aligned, axis=0)

    def average(self, weights=None, returned=False):
        t_first, aligned = self.aligned()
        average, weights = np.average(aligned, axis=0, weights=weights, returned=returned)
        return t_first, average, weights

    def correct_values(self, correction_factors):
        for ii,var_name in enumerate(self.variable_list):
            self.timber_variables[var_name].values = self.timber_variables[var_name].values*correction_factors[ii]
