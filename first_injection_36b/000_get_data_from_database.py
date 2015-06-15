
import sys, os
BIN = os.path.expanduser("../")
sys.path.append(BIN)

import TimberManager as tm
import LHC_FBCT
import timestamp_helpers as th

import numpy as np

t_start_string = '2015_06_14 19:30:00'
t_end_string = '2015_06_14 21:30:00'

t_obs_b1 = np.arange(24.5, 64.6, 5)
t_obs_b2 = np.arange(32.5, 76.5, 5)


filename = 'logged_data.csv'


t_start = th.localtime2unixstamp(t_start_string)
t_end = th.localtime2unixstamp(t_end_string)

t_ref = t_start

variables_to_download = LHC_FBCT.variable_list()

#tm.dbquery(varlist = variables_to_download, t_start=t_start, t_stop=t_end, filename = filename)


fbct_b1 = LHC_FBCT.FBCT(filename, beam=1)
fbct_b2 = LHC_FBCT.FBCT(filename, beam=2)

import pylab as pl

pl.close('all')
pl.figure(100)
pl.plot((fbct_b1.tstamps-t_ref)/60.,fbct_b1.totint, '.-b')
pl.plot((fbct_b2.tstamps-t_ref)/60.,fbct_b2.totint, '.-r')



for ii in xrange(len(t_obs_b1)):
	bunch_inten, t_meas = fbct_b1.nearest_older_sample(t_obs=(t_ref+t_obs_b1[ii]*60), flag_return_time=True)

	pl.figure(1)
	pl.plot(bunch_inten, 'o')
	pl.grid('on')
	
	
for ii in xrange(len(t_obs_b2)):
	bunch_inten, t_meas = fbct_b2.nearest_older_sample(t_obs=(t_ref+t_obs_b2[ii]*60), flag_return_time=True)

	pl.figure(2)
	pl.plot(bunch_inten, 'o')
	pl.grid('on')

pl.show()
