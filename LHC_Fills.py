import numpy as np
import TimberManager as tm
import pickle


class fillnumber:
    def __init__(self,filename):
        if type(filename) is str:
            dict_timber_filln = tm.parse_timber_file(filename)
        else:
            dict_timber_filln = filename
        self.t_stamps = np.array(map(float, dict_timber_filln['HX:FILLN'].t_stamps))
        self.filln = np.array(map(lambda x: int(x[0]),dict_timber_filln['HX:FILLN'].values))

    def fill_start_end(self, filln_to_find):
        i_found = np.where(self.filln==filln_to_find)[0][0]
        return self.t_stamps[i_found], self.t_stamps[i_found+1]


def make_pickle(csv_filename, pkl_filename):
    dict_fbm = tm.parse_timber_file(csv_filename)
    filln_obj = fillnumber(dict_fbm)

    list_b_modes = []
    for kk in dict_fbm.keys():
	if 'HX:BMODE_' in kk:
            list_b_modes.append(kk.split(':BMODE_')[-1])
		
    dict_t_start_stop_vects = {}
    for bmode in list_b_modes:
	flag_bmode = np.squeeze(np.float_(np.array(dict_fbm['HX:BMODE_'+bmode].values)))
	diff_flag_bmode = np.diff(flag_bmode)
	t_diff_flag_bmode = np.array(dict_fbm['HX:BMODE_'+bmode].t_stamps)[1:];
	dict_t_start_stop_vects['t_start_'+bmode] = t_diff_flag_bmode[diff_flag_bmode == 1.]
	dict_t_start_stop_vects['t_stop_'+bmode] = t_diff_flag_bmode[diff_flag_bmode == -1.]

    fill_n_list = list(filln_obj.filln[filln_obj.filln > 0])
    dict_fill_bmodes = {}

    for ii in xrange(len(fill_n_list) - 1):
	filln = fill_n_list[ii]
	print 'filln = %d'%filln
	dict_fill_bmodes[filln] = {}

	t_startfill, t_endfill = filln_obj.fill_start_end(filln)
	dict_fill_bmodes[filln]['t_startfill'] = t_startfill
	dict_fill_bmodes[filln]['t_endfill'] = t_endfill

	for bmode in list_b_modes:
            dict_fill_bmodes[filln]['t_start_'+bmode] = -1.
            dict_fill_bmodes[filln]['t_stop_'+bmode] = -1.
            ii_start_bmode = np.where(np.logical_and(dict_t_start_stop_vects['t_start_'+bmode] > t_startfill, 
                                                     dict_t_start_stop_vects['t_start_'+bmode] < t_endfill))[0]
            if len(ii_start_bmode) > 0:
                dict_fill_bmodes[filln]['t_start_'+bmode] = dict_t_start_stop_vects['t_start_'
                                                                                    +bmode][ii_start_bmode[0]]

            ii_stop_bmode = np.where(np.logical_and(dict_t_start_stop_vects['t_stop_'+bmode] > t_startfill, 
                                                    dict_t_start_stop_vects['t_stop_'+bmode] < t_endfill))[0]
            if len(ii_start_bmode) > 0:
                dict_fill_bmodes[filln]['t_stop_'+bmode] = dict_t_start_stop_vects['t_stop_'
                                                                                   +bmode][ii_start_bmode[0]]

    with open(pkl_filename, 'wb') as fid:
	pickle.dump(dict_fill_bmodes, fid)


def get_varlist():
    varlist = ['HX:FILLN',
               'HX:BMODE',
               'HX:BMODE_ABORT',
               'HX:BMODE_SQUEEZE',
               'HX:BMODE_PRERAMP',
               'HX:BMODE_SETUP',
               'HX:BMODE_WBDUMP',
               'HX:BMODE_NOMODE',
               'HX:BMODE_ADJUST',
               'HX:BMODE_INJPHYS',
               'HX:BMODE_CIRCDUMP',
               'HX:BMODE_RAMP',
               'HX:BMODE_FLATTOP',
               'HX:BMODE_INJSTUP',
               'HX:BMODE_INJDUMP',
               'HX:BMODE_NOBEAM',
               'HX:BMODE_STABLE',
               'HX:BMODE_INJPROT',
               'HX:BMODE_CYCLING',
               'HX:BMODE_UNSTABLE',
               'HX:BMODE_RECOVERY',
               'HX:BMODE_RAMPDOWN',
               'HX:BMODE_BEAMDUMP']

    return varlist
 
