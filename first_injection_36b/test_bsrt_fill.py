import sys, os
BIN = os.path.expanduser("../")
sys.path.append(BIN)

import LHC_FBCT as FBCT
import LHC_Energy as Energy
import LHC_BSRT as BSRT
import LHC_Fills as Fills
import mystyle as ms
import numpy as np
import pylab as pl
import time
from colorsys import hsv_to_rgb


filln = 3859
scan_thrld = 100
list_scan_times = np.linspace(2.33, 2.98, 15) 
# first_obs_buck = [0, 0, 0, 0, 0]
# last_obs_buck = [3500, 3500, 3500, 3500, 3500]

fills_ob = Fills.fillnumber('fills_and_bmodes.csv')
BSRT_ob = BSRT.BSRT('BSRT_test_36b.csv', beam=1)
fill_file = 'fill_%d.csv'%filln
intensity_ob = FBCT.FBCT(fill_file, beam=1)
energy_ob = Energy.energy(fill_file, beam=1)

t_stamps_BSRT = BSRT_ob.t_stamps
bunch_n_BSRT = BSRT_ob.bunch_n
sigma_h = BSRT_ob.sigma_h
sigma_v = BSRT_ob.sigma_v

BSRT_ob.calculate_emittances(energy_ob)
norm_emit_h = BSRT_ob.norm_emit_h
norm_emit_v = BSRT_ob.norm_emit_v

#find start scan

# diff_nbun = np.diff(bunch_n_BSRT)
# indices_start_scan_all = np.where(diff_nbun<-scan_thrld)[0]
# indices_start_scan = indices_start_scan_all[np.diff(indices_start_scan_all)>10]
# t_start_scans = t_stamps_BSRT[indices_start_scan]
# t_start_scans = BSRT_ob.find_start_scans(scan_thrld)


pl.close('all')

# pl.figure(100)
# sp1= pl.subplot(2,1,1)
# pl.plot(bunch_n_BSRT)
# pl.subplot(2,1,2, sharex=sp1)
# pl.plot(diff_nbun)
# pl.plot(indices_start_scan_all, diff_nbun[indices_start_scan_all], '.r')
# pl.plot(indices_start_scan, diff_nbun[indices_start_scan], '.g')
# pl.show()

t_fill_st, t_fill_end = fills_ob.fill_start_end(filln)
t_fill_len = t_fill_end - t_fill_st
t_ref = t_fill_st
mask_curr_fill = np.logical_and(t_stamps_BSRT >= t_fill_st, t_stamps_BSRT < t_fill_end)

fig_h = pl.figure(1)
ms.mystyle()

sp_tot_int = pl.subplot2grid((2,3), (0, 0), rowspan=1)
pl.plot((intensity_ob.t_stamps - t_ref)/3600., intensity_ob.totint*1e-13, 'b')
pl.plot((energy_ob.t_stamps - t_ref)/3600, energy_ob.energy/1e3, 'k')
pl.ylabel('Inten. [p x10^13], Energy [TeV]')
pl.xlim(0, t_fill_len/3600.)

sp_acq_bunch = pl.subplot2grid((2,3), (1, 0), rowspan=1, sharex=sp_tot_int)
pl.plot((t_stamps_BSRT[mask_curr_fill] - t_ref)/3600., bunch_n_BSRT[mask_curr_fill], 'b')
pl.ylabel('Acq. bunch')
pl.xlabel('Time [h]')
pl.ylim(0,1200)
# pl.ylim(0,3500)
pl.xlim(2.0, 3.1)
# pl.xlim(0, t_fill_len/3600.)

N_scans = len(list_scan_times)

sp_ssigma_h = pl.subplot2grid((2,3), (0, 1), rowspan=1, colspan=2)
sp_ssigma_v = pl.subplot2grid((2,3), (1, 1), rowspan=1, colspan=2, sharex = sp_ssigma_h)

for ii in xrange(N_scans):
    colorcurr = hsv_to_rgb(float(ii)/float(N_scans), 0.9, 1.)
	
    # find closer scan
    t_start_requested = list_scan_times[ii]*3600.+t_ref
    # ind_closer_scan = np.argmin(np.abs(t_start_requested-t_start_scans))
    
    # t_start_trace_curr = t_start_scans[ind_closer_scan]
    # t_stop_trace_curr = t_start_scans[ind_closer_scan+1]
    # mask_BSRT_curr_scan = np.logical_and(t_stamps_BSRT>=t_start_trace_curr, t_stamps_BSRT<t_stop_trace_curr)

    mask_curr_scan = BSRT_ob.find_closest_scan_mask(t_start_requested, scan_thrld)
    
    sp_ssigma_h.plot(bunch_n_BSRT[mask_curr_scan], norm_emit_h[mask_curr_scan], '.', color=colorcurr)
    sp_ssigma_v.plot(bunch_n_BSRT[mask_curr_scan], norm_emit_v[mask_curr_scan], '.', color=colorcurr)
	
    # sp_ssigma_h.plot(bunch_n_BSRT[mask_curr_scan], sigma_h[mask_curr_scan], '.', color=colorcurr)
    # sp_ssigma_v.plot(bunch_n_BSRT[mask_curr_scan], sigma_v[mask_curr_scan], '.', color=colorcurr)
	 
	
    sp_acq_bunch.axvspan((BSRT_ob.t_start_trace_curr - t_ref)/3600., (BSRT_ob.t_stop_trace_curr-t_ref)/3600., facecolor=colorcurr, alpha=0.5)
    sp_tot_int.axvspan((BSRT_ob.t_start_trace_curr - t_ref)/3600., (BSRT_ob.t_stop_trace_curr-t_ref)/3600., facecolor=colorcurr, alpha=0.5)
	
    sp_acq_bunch.axvline((BSRT_ob.t_start_trace_curr - t_ref)/3600., color=colorcurr)
    sp_tot_int.axvline((BSRT_ob.t_start_trace_curr - t_ref)/3600., color=colorcurr)
	
sp_ssigma_h.set_xlim(1000, 1200)
# sp_ssigma_h.set_ylim(0, 3.)
sp_ssigma_h.set_xlabel('25 ns slot')
sp_ssigma_h.set_ylabel('Horizontal emittance [um]')
# sp_ssigma_h.set_ylabel('Sigma H')

sp_ssigma_v.set_xlim(1000, 1200)
# sp_ssigma_v.set_ylim(0, 3.)
sp_ssigma_v.set_xlabel('25 ns slot')
sp_ssigma_v.set_ylabel('Vertical emittance [um]')
# sp_ssigma_v.set_ylabel('Sigma V')

tref_string = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t_ref))
pl.suptitle('B1 Fill. %d started on %s'%(filln, tref_string))
pl.subplots_adjust(top=0.85,right=0.95, left=0.09, hspace=0.45, wspace=0.25)	
fig_h.set_size_inches(15., 8.)

filename_out = 'Fill_%d_BSRT_B1.png'%filln
pl.savefig(filename_out)
	
pl.show()





