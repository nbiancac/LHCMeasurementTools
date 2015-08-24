import numpy as np
import TimberManager as tm


class BBQ(object):

    def __init__(self, timber_variable_bbq, beam=0):

        if not (beam == 1 or beam == 2):
            raise ValueError('You need to specify which beam! (1 or 2)')
        self.beam = beam

        if type(timber_variable_bbq) is dict:
            dict_timber = timber_variable_bbq
        else:
            dict_timber = tm.parse_timber_file(timber_variable_bbq, verbose=True)

        self.t_stamps = np.squeeze(np.array(
            dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_AMPL_1'.format(beam)].t_stamps))
        self.amp_1 = np.squeeze(np.array(
            dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_AMPL_1'.format(beam)].values))
        self.amp_2  = np.squeeze(np.array(
            dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_AMPL_2'.format(beam)].values))
        self.xamp_1 = np.squeeze(np.array(
            dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_X_AMPL_1'.format(beam)].values))
        self.xamp_2 = np.squeeze(np.array(
            dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_X_AMPL_2'.format(beam)].values))

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

    def convert_to_array(self, v):

        v.t_stamps = np.squeeze(np.array(v.t_stamps, dtype='float_'))
        v.values   = np.squeeze(np.array(v.values, dtype='float_'))


class BBQ_FFT(object):

    def __init__(self, timber_variable_bbq, beam=0):

        if not (beam == 1 or beam == 2):
            raise ValueError('You need to specify which beam! (1 or 2)')
        self.beam = beam

        if type(timber_variable_bbq) is dict:
            dict_timber = timber_variable_bbq
        else:
            dict_timber = tm.parse_timber_file(timber_variable_bbq, verbose=True)

        self.fft_h  = dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:FFT_DATA_H'.format(beam)]
        self.fft_v  = dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:FFT_DATA_V'.format(beam)]
        self.tune_h  = dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_FREQ_1'.format(beam)]
        self.tune_v  = dict_timber['LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_FREQ_2'.format(beam)]
      #  self.fft_h  = self.convert_to_array(self.fft_h)
     #   self.fft_v  = self.convert_to_array(self.fft_v)

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

    def convert_to_array(self, v):

        v.t_stamps = np.squeeze(np.array(v.t_stamps, dtype='float_'))
        v.values   = np.squeeze(np.array(v.values, dtype='float_'))


def get_variable_dict(beam):
    print beam
    var_dict = {}
    var_dict['BBQ_HS_AMPL_1'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_AMPL_1'.format(beam)
    var_dict['BBQ_HS_AMPL_2'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_AMPL_2'.format(beam)
    var_dict['BBQ_HS_FREQ_1'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_FREQ_1'.format(beam)
    var_dict['BBQ_HS_FREQ_2'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_FREQ_2'.format(beam)
    var_dict['BBQ_HS_WIDTH_1'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_WIDTH_1'.format(beam)
    var_dict['BBQ_HS_WIDTH_2'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_WIDTH_2'.format(beam)
    var_dict['BBQ_HS_X_AMPL_1'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_X_AMPL_1'.format(beam)
    var_dict['BBQ_HS_X_AMPL_2'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:EIGEN_X_AMPL_2'.format(beam)
    var_dict['BBQ_HS_FFT_H'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:FFT_DATA_H'.format(beam)
    var_dict['BBQ_HS_FFT_V'] = 'LHC.BQBBQ.CONTINUOUS_HS.B{:d}:FFT_DATA_V'.format(beam)

    return var_dict


def variable_list(beams = [1, 2]):
    var_list = []
    for beam in beams:
        var_list += get_variable_dict(beam).values()

    return var_list
