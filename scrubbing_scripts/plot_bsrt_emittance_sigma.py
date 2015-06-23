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
beam = 1
plot_emittance = True

fills_bmodes_file = 'fills_and_bmodes.csv'
fill_file = 'fill_%d.csv'%filln
fbct_file = fille_file
bsrt_file = fill_file

fills_bmodes = Fills.fillnumber(fills_bmodes_file)
energy = Energy.energy(fill_file, beam=beam)
intensity = FBCT.FBCT(fbct_file, beam=beam)
bsrt  = BSRT.BSRT(bsrt_file, beam=beam)
if plot_emittance:
    bsrt.calculate_emittances(energy)


t_fill_st, t_fill_end = fills_bmodes.fill_start_end(filln)
t_fill_len = t_fill_end - t_fill_st
t_ref = t_fill_st

# START PLOT
fig_h = pl.figure(1)
ms.mystyle()

# Intensity and energy
sp_int = pl.subplot2grid((2,3), (0, 0), rowspan=1)
sp_energy = sp_int.twinx()

sp_int.plot((intensity.t_stamps - t_ref)/3600., intensity.totint, 'b')
sp_energy.plot((energy.t_stamps - t_ref)/3600, energy.energy/1e3, 'k')

sp_int.set_ylabel('Intensity [p$^+$]')
sp_energy.set_ylabel('Energy [TeV]')
sp_int.set_xlim(0, t_fill_len/3600.)

# Bunches
fill = BSRT.Masked(bsrt, t_fill_st, t_fill_end)
sp_bunch = pl.subplot2grid((2,3), (1, 0), rowspan=1, sharex = sp_int)

pl.plot((fill.t_stamps - t_ref)/3600., fill.bunch_n, 'b')

pl.ylabel('Acq. bunch')
pl.xlabel('Time [h]')
pl.ylim(0,1200)
pl.xlim(2.0, 3.1)
# pl.xlim(0, t_fill_len/3600.)


# Sigma and emittance
N_scans = len(list_scan_times)
sp_sigma_h = pl.subplot2grid((2,3), (0, 1), rowspan=1, colspan=2)
sp_sigma_v = pl.subplot2grid((2,3), (1, 1), rowspan=1, colspan=2, sharex = sp_sigma_h)

for ii in xrange(N_scans):
    colorcurr = hsv_to_rgb(float(ii)/float(N_scans), 0.9, 1.)
	
    t_start_requested = list_scan_times[ii]*3600. + t_ref
    scan = bsrt.find_closest_scan(t_start_requested, scan_thrld)

    if plot_emittance:    
        sp_sigma_h.plot(scan.bunch_n, scan.norm_emit_h, '.', color=colorcurr)
        sp_sigma_v.plot(scan.bunch_n, scan.norm_emit_v, '.', color=colorcurr)
	
    else:
        sp_sigma_h.plot(scan.bunch_n, scan.sigma_h, '.', color=colorcurr)
        sp_sigma_v.plot(scan.bunch_n, scan.sigma_v, '.', color=colorcurr)
	 	
    sp_bunch.axvspan((scan.t_start - t_ref)/3600., (scan.t_stop - t_ref)/3600., facecolor=colorcurr, alpha=0.5)
    sp_int.axvspan((scan.t_start - t_ref)/3600., (scan.t_stop - t_ref)/3600., facecolor=colorcurr, alpha=0.5)
	
    sp_bunch.axvline((scan.t_start - t_ref)/3600., color=colorcurr)
    sp_int.axvline((scan.t_start - t_ref)/3600., color=colorcurr)
	
sp_sigma_h.set_xlim(1000, 1200)
sp_sigma_v.set_xlim(1000, 1200)
# sp_sigma_h.set_ylim(0, 3.)
# sp_sigma_v.set_ylim(0, 3.)
sp_sigma_h.set_xlabel('25 ns slot')
sp_sigma_v.set_xlabel('25 ns slot')
if plot_emittance:
    sp_sigma_h.set_ylabel('Hor. emittance [um]')
    sp_sigma_v.set_ylabel('Vert. emittance [um]')
    plot_str = 'emittance'
else:
    sp_sigma_h.set_ylabel('Hor. sigma [a.u.]')
    sp_sigma_v.set_ylabel('Vert. sigma [a.u.]')
    plot_str = 'sigma'

tref_string = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(t_ref))
fig_h.suptitle('Fill %d: B%d, started on %s'%(filln, bsrt.beam, tref_string))
fig_h.subplots_adjust(top=0.85,right=0.95, left=0.07, hspace=0.40, wspace=0.35)	
fig_h.set_size_inches(16., 8.)

filename_out = 'Fill_%d_BSRT_B1_%s.png'%(filln,plot_str)
pl.savefig(filename_out)
	
pl.show()
