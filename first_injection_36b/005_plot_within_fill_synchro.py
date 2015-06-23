import numpy as np
import pylab as pl
import mystyle as ms
import myloadmat as mlm
import fill_number_vector_class as fnvc
from colorsys import hsv_to_rgb
import time

#~ filln = 3425
#~ scan_thrld=200
#~ list_scan_times = [1.31]+list(np.arange(1.58, 4.81, 1.))

#~ filln = 3427
#~ scan_thrld=500
#~ list_scan_times = [1.45]+[1.76, 2.5]

#~ filln = 3428
#~ scan_thrld=1000
#~ list_scan_times = [1.45]+list(np.arange(1.76, 3.9, 1.))


#~ filln = 3429
#~ scan_thrld=1000
#~ list_scan_times = [2.11]+list(np.arange(2.54, 12.05, 1.))

#~ filln = 3436
#~ scan_thrld=1000
#~ list_scan_times = [.7, .93]+list(np.arange(1.34, 2.36, 1.))

#~ filln = 3437
#~ scan_thrld=1000
#~ list_scan_times = [.7, .93]+list(np.arange(1.34, 2.36, 1.))

#~ filln = 3441
#~ scan_thrld=1000
#~ list_scan_times = [2.24, 2.36]+list(np.arange(2.6, 4.64, 1.))

#~ filln = 3442
#~ scan_thrld=1000
#~ list_scan_times = [1.98]+list(np.arange(2.3, 4.76, 1.))

#~ filln = 3453
#~ scan_thrld=1000
#~ list_scan_times = [1.997]+list(np.arange(2.37, 10.92, 1.))

filln = 3457
scan_thrld=1000
list_scan_times = [0., .47, .85]
first_obs_buck = [0, 0, 1750]
last_obs_buck = [3500, 1750, 3500]

ene_and_int = mlm.myloadmat('../../hl_plot_for_cmac/ener_intensities15days.mat')
fillnobj = fnvc.fillnumber('Fill_number_dec2012.csv')

BSRT_dict = mlm.myloadmat('BRST_dec2012.mat')
t_stamps_BSRT = BSRT_dict['t_stamp_UNIX']
bunch_n_BSRT = BSRT_dict['bunch_n']
norm_emit_h = BSRT_dict['norm_emit_h']
norm_emit_v = BSRT_dict['norm_emit_v']

sigma_h = BSRT_dict['sigma_h']
sigma_v = BSRT_dict['sigma_v']


t_fill_st, t_fill_end = fillnobj.fill_start_end(filln)
t_fill_len = t_fill_end - t_fill_st

t_ref = t_fill_st

#find start scan

diff_nbun = np.diff(bunch_n_BSRT)
indices_start_scan_all = np.where(diff_nbun<-scan_thrld)[0]
indices_start_scan = indices_start_scan_all[np.diff(indices_start_scan_all)>10]
t_start_scans = t_stamps_BSRT[indices_start_scan]

pl.close('all')

pl.figure(100)
sp1= pl.subplot(2,1,1)
pl.plot(bunch_n_BSRT)
pl.subplot(2,1,2, sharex=sp1)
pl.plot(diff_nbun)
pl.plot(indices_start_scan_all,diff_nbun[indices_start_scan_all],'.r')
pl.plot(indices_start_scan,diff_nbun[indices_start_scan],'.g')


pl.show()



fig_h = pl.figure(1)
ms.mystyle()
sp_tot_int=pl.subplot2grid((2,3), (0, 0), rowspan=1)
pl.plot((ene_and_int['t_stamps_b1']-t_ref)/3600.,ene_and_int['int_b1']*1e-13, 'b')
pl.plot((ene_and_int['t_stamps_ene']-t_ref)/3600, ene_and_int['energy']/1e3, 'k')
pl.ylabel('Inten. [p x10^13], Energy [TeV]')
pl.xlim(0, t_fill_len/3600.)


mask_BSRT_curr_fill = np.logical_and(t_stamps_BSRT>=t_fill_st, t_stamps_BSRT<t_fill_end)
sp_acq_bunch=pl.subplot2grid((2,3), (1, 0), rowspan=1, sharex=sp_tot_int)
pl.plot((t_stamps_BSRT[mask_BSRT_curr_fill]-t_ref)/3600.,bunch_n_BSRT[mask_BSRT_curr_fill], 'b')
pl.ylabel('Acq. bunch')
pl.xlabel('Time [h]')
pl.ylim(0,3500)
pl.xlim(0, t_fill_len/3600.)

N_scans = len(list_scan_times)

sp_ssigma_h = pl.subplot2grid((2,3), (0, 1), rowspan=1, colspan=2)
sp_ssigma_v = pl.subplot2grid((2,3), (1, 1), rowspan=1, colspan=2, sharex = sp_ssigma_h)

for ii in xrange(N_scans):
	colorcurr = hsv_to_rgb(float(ii)/float(N_scans), 0.9, 1.)
	
	#find closer scan
	t_start_requested = list_scan_times[ii]*3600.+t_ref
	ind_closer_scan = np.argmin(np.abs(t_start_requested-t_start_scans))
	
	t_start_trace_curr = t_start_scans[ind_closer_scan]
	t_stop_trace_curr = t_start_scans[ind_closer_scan+1]
	mask_BSRT_curr_scan = np.logical_and(t_stamps_BSRT>=t_start_trace_curr, t_stamps_BSRT<t_stop_trace_curr)
	
	sp_ssigma_h.plot(bunch_n_BSRT[mask_BSRT_curr_scan],norm_emit_h[mask_BSRT_curr_scan], '.', color=colorcurr)
	sp_ssigma_v.plot(bunch_n_BSRT[mask_BSRT_curr_scan], norm_emit_v[mask_BSRT_curr_scan], '.', color=colorcurr)
	
	#~ sp_ssigma_h.plot(bunch_n_BSRT[mask_BSRT_curr_scan],sigma_h[mask_BSRT_curr_scan], '.', color=colorcurr)
	#~ sp_ssigma_v.plot(bunch_n_BSRT[mask_BSRT_curr_scan], sigma_v[mask_BSRT_curr_scan], '.', color=colorcurr)
	#~ 
	
	sp_acq_bunch.axvspan((t_start_trace_curr-t_ref)/3600., (t_stop_trace_curr-t_ref)/3600., facecolor=colorcurr, alpha=0.5)
	sp_tot_int.axvspan((t_start_trace_curr-t_ref)/3600., (t_stop_trace_curr-t_ref)/3600., facecolor=colorcurr, alpha=0.5)
	
	sp_acq_bunch.axvline((t_start_trace_curr-t_ref)/3600., color=colorcurr)
	sp_tot_int.axvline((t_start_trace_curr-t_ref)/3600., color=colorcurr)
	
	
sp_ssigma_h.set_xlim(0, 3500)
sp_ssigma_h.set_ylim(0, 6.)
sp_ssigma_h.set_xlabel('25 ns slot')
sp_ssigma_h.set_ylabel('Horizontal emittance [um]')

sp_ssigma_v.set_xlim(0, 3500)
sp_ssigma_v.set_ylim(0, 6.)
sp_ssigma_v.set_xlabel('25 ns slot')
sp_ssigma_v.set_ylabel('Vertical emittance [um]')

tref_string=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t_ref))
pl.suptitle('B1 Fill. %d started on %s'%(filln, tref_string))
pl.subplots_adjust(top=0.85,right=0.95, left=0.09, hspace=0.45, wspace=0.25)	
fig_h.set_size_inches(15., 8.)

filename_out = 'efill%d_BSRT_B1.png'%filln
pl.savefig(filename_out)
	
pl.show()





