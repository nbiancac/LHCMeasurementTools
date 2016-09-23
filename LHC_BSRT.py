
import numpy as np
import TimberManager as tm
import datetime

class BSRT:
    def __init__(self, timber_variable_bsrt, beam=0):

        # assume timber_variable_bsrt is filename string for now
        if not (beam == 1 or beam == 2):
            raise ValueError('You need to specify which beam! (1 or 2)')
        self.beam = beam
        if type(timber_variable_bsrt) is dict:
            dict_timber = timber_variable_bsrt
        else:
            dict_timber = tm.parse_timber_file(timber_variable_bsrt, verbose=True)

        sigma_h = dict_timber[get_variable_dict(beam)['SIGMA_H']]
        sigma_v = dict_timber[get_variable_dict(beam)['SIGMA_V']]
        gate = dict_timber[get_variable_dict(beam)['GATE_DELAY']]
        
        if np.all(sigma_h[0] != sigma_v[0]):
            raise Warning('Timestamps for the two channels (H and V) not equal!')
        if np.all(sigma_v[0] != gate[0]):
            bunches_effectively_recorded = self.get_bunches_effectively_recorded(gate, sigma_v)
        else:
            bunches_effectively_recorded = gate

        self.t_stamps = []
        self.bunch_n = []
        self.sigma_h = []
        self.sigma_v = []
        
        for ii in xrange(len(bunches_effectively_recorded[0])):
            if np.mod(ii,10000) == 0:
                print 'expanding %.1f'%(float(ii)/len(bunches_effectively_recorded[0])*100) + """%"""

            N_meas = len(bunches_effectively_recorded[1][ii])
            for jj in xrange(N_meas):
                self.bunch_n.append(np.float_(bunches_effectively_recorded[1][ii][jj]))
                self.sigma_h.append(np.float_(sigma_h[1][ii][jj]))
                self.sigma_v.append(np.float_(sigma_v[1][ii][jj]))
                self.t_stamps.append(np.float_(sigma_v[0][ii]) + float(jj)*1e-3/float(N_meas))

        self.t_stamps = np.array(self.t_stamps)
        self.bunch_n = np.array(self.bunch_n)
        self.sigma_h = np.array(self.sigma_h)
        self.sigma_v = np.array(self.sigma_v)
        self.t_str=np.array([datetime.datetime.fromtimestamp(self.t_stamps[ii]) for ii in np.arange(len(self.t_stamps))])
    
    def calculate_emittances(self, energy_ob, filln):
        e_dict = emittance_dictionary(filln)
        self.norm_emit_h = []
        self.norm_emit_v = []
        for ii in xrange(len(self.t_stamps)):
            if np.mod(ii,10000)==0:
                print 'calc. emitt. %.1f'%(float(ii)/len(self.t_stamps)*100)+"""%"""

            norm_emit_h  = 0.
            norm_emit_v  = 0.

            energy = energy_ob.nearest_older_sample(self.t_stamps[ii])
            if energy > 400. and energy < 500.:
                energy = 450.
            elif energy > 6400. and energy < 6600.:
                energy = 6500.
            else:
                self.norm_emit_h.append(norm_emit_h)
                self.norm_emit_v.append(norm_emit_v)
                continue

            sigma_h_corr_sq = self.sigma_h[ii]**2 - e_dict['sigma_corr_h'][energy][self.beam]**2
            sigma_v_corr_sq = self.sigma_v[ii]**2 - e_dict['sigma_corr_v'][energy][self.beam]**2

            phys_emit_h = sigma_h_corr_sq/e_dict['betaf_h'][energy][self.beam]
            phys_emit_v = sigma_v_corr_sq/e_dict['betaf_v'][energy][self.beam]

            norm_emit_h  = phys_emit_h*e_dict['gamma'][energy]
            norm_emit_v  = phys_emit_v*e_dict['gamma'][energy]

            self.norm_emit_h.append(norm_emit_h)
            self.norm_emit_v.append(norm_emit_v)

        self.norm_emit_h = np.array(self.norm_emit_h)
        self.norm_emit_v = np.array(self.norm_emit_v)


    def find_start_scans(self, scan_thresh):
        diff_bunch = np.diff(self.bunch_n)
        ind_start_scan_all = np.where(diff_bunch < -scan_thresh)[0]
        ind_start_scan = ind_start_scan_all[np.diff(ind_start_scan_all) > 10]
        self.t_start_scans = self.t_stamps[ind_start_scan]
        self.t_start_scans = np.array(list(self.t_start_scans)+[self.t_stamps[-1]])

        # return self.t_start_scans


    def find_closest_scan(self, t_start_requested, scan_thresh):
        self.find_start_scans(scan_thresh)
        ind_closest_scan = np.argmin(np.abs(t_start_requested - self.t_start_scans))
        t_start = self.t_start_scans[ind_closest_scan]
        if ind_closest_scan + 1 >= len(self.t_start_scans):
            raise IndexError('Index ind_closest_scan + 1 is out of bounds.\nYour requested scan times might be outside of the fill.')
        t_stop = self.t_start_scans[ind_closest_scan + 1]
        return Masked(self, t_start, t_stop)

    def get_bunches_effectively_recorded(self):
        print 'cleaning ...'
        ind_clean = np.where((self.bunch_n == 0 ) & (self.sigma_h == 0))[0]
        self.bunch_n =     np.delete(self.bunch_n,ind_clean)
        self.norm_emit_h = np.delete(self.norm_emit_h,ind_clean)
        self.norm_emit_v = np.delete(self.norm_emit_v, ind_clean)
        self.sigma_h =     np.delete(self.sigma_h,ind_clean) 
        self.sigma_v =     np.delete(self.sigma_v,ind_clean)
        self.t_stamps =    np.delete(self.t_stamps,ind_clean)
        self.t_str =       np.delete(self.t_str,ind_clean) 
        
    
#     def get_bunches_effectively_recorded(self, gate_timber, sigma_timber):
#         recorded_bunches = tm.timber_variable_list()
#         i1 = 0
#         for i2 in xrange(len(gate_timber.t_stamps)):
#             if np.mod(i2,10000) == 0:
#                 print 'Cleaning %.1f'%(float(i2)/len(gate_timber.t_stamps)*100)+"""%"""
#             if gate_timber.t_stamps[i2] == sigma_timber.t_stamps[i1]:
#                 recorded_bunches.t_stamps.append(gate_timber.t_stamps[i2])
#                 recorded_bunches.values.append(gate_timber.values[i2])
#                 i1 += 1

#         return recorded_bunches


class Masked:
    def __init__(self, bsrt, t_start, t_stop):
        self.t_start = t_start
        self.t_stop = t_stop
        mask_bsrt = np.logical_and(bsrt.t_stamps >= self.t_start, bsrt.t_stamps < self.t_stop)

        self.beam = bsrt.beam
        self.t_stamps = bsrt.t_stamps[mask_bsrt]
        self.t_str = bsrt.t_str[mask_bsrt]
        self.bunch_n = bsrt.bunch_n[mask_bsrt]
        self.sigma_h = bsrt.sigma_h[mask_bsrt]
        self.sigma_v = bsrt.sigma_v[mask_bsrt]
        if hasattr(bsrt, 'norm_emit_h'):
            self.norm_emit_h = bsrt.norm_emit_h[mask_bsrt]
            self.norm_emit_v = bsrt.norm_emit_v[mask_bsrt]

def emittance_dictionary(filln):
 e_dict = {'betaf_h':{}, 'betaf_v':{}, 'gamma':{},
              'sigma_corr_h':{}, 'sigma_corr_v':{}}
    
 if filln<5256:
        e_dict = {'betaf_h':{}, 'betaf_v':{}, 'gamma':{},
                  'sigma_corr_h':{}, 'sigma_corr_v':{}}
        for kk in e_dict.keys():
            e_dict[kk] = {450:{}, 6500:{}}

        # Beam 1:
        e_dict['betaf_h'][450][1] = 204.1
        e_dict['betaf_h'][6500][1] = 200.
        e_dict['betaf_v'][450][1] = 317.3
        e_dict['betaf_v'][6500][1] = 330.
        e_dict['sigma_corr_h'][450][1] = 0.528
        e_dict['sigma_corr_h'][6500][1] = 0.303
        e_dict['sigma_corr_v'][450][1] = 0.437
        e_dict['sigma_corr_v'][6500][1] = 0.294

        # Beam 2:
        e_dict['betaf_h'][450][2] = 200.6
        e_dict['betaf_h'][6500][2] = 200.
        e_dict['betaf_v'][450][2] = 327.1
        e_dict['betaf_v'][6500][2] = 330.
        e_dict['sigma_corr_h'][450][2] = 0.518
        e_dict['sigma_corr_h'][6500][2] = 0.299
        e_dict['sigma_corr_v'][450][2] = 0.675
        e_dict['sigma_corr_v'][6500][2] = 0.299

        # gamma
        e_dict['gamma'][450] = 479.6
        e_dict['gamma'][6500] = 6927.6
       
 else:
        e_dict = {'betaf_h':{}, 'betaf_v':{}, 'gamma':{},
                  'sigma_corr_h':{}, 'sigma_corr_v':{}}
        for kk in e_dict.keys():
            e_dict[kk] = {450:{}, 6500:{}}

        # Beam 1:
        e_dict['betaf_h'][450][1] = 204.1
        e_dict['betaf_h'][6500][1] = 200.
        e_dict['betaf_v'][450][1] = 317.3
        e_dict['betaf_v'][6500][1] = 330.
        e_dict['sigma_corr_h'][450][1] = .52
        e_dict['sigma_corr_h'][6500][1] = .32
        e_dict['sigma_corr_v'][450][1] = .68
        e_dict['sigma_corr_v'][6500][1] = .34

        # Beam 2:
        e_dict['betaf_h'][450][2] = 200.6
        e_dict['betaf_h'][6500][2] = 200.
        e_dict['betaf_v'][450][2] = 327.1
        e_dict['betaf_v'][6500][2] = 330.
        e_dict['sigma_corr_h'][450][2] = .47
        e_dict['sigma_corr_h'][6500][2] = .32
        e_dict['sigma_corr_v'][450][2] = .64
        e_dict['sigma_corr_v'][6500][2] = .3

        # gamma
        e_dict['gamma'][450] = 479.6
        e_dict['gamma'][6500] = 6927.6


 return e_dict


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