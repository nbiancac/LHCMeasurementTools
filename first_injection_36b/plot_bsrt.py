import sys, os
BIN = os.path.expanduser("../")
sys.path.append(BIN)

import TimberManager as tm
import LHC_BSRT
import mystyle as ms
import numpy as np
import pylab as pl

t_ref_str = '2015-06-14 17:30:00'
t_ref = tm.timb_timestamp2float_UTC(t_ref_str)

bsrt_ob = LHC_BSRT.BSRT('BSRT_test_36b.csv', beam=1)

pl.close('all')
pl.figure(1)
ms.mystyle()
sp1 = pl.subplot(2,1,1)
pl.plot((bsrt_ob.t_stamps - t_ref)/3600., bsrt_ob.bunch_n, 'r')
pl.ylabel('Acquired bunch')

pl.subplot(2,1,2, sharex = sp1)
pl.plot((bsrt_ob.t_stamps - t_ref)/3600., bsrt_ob.sigma_h, 'b')
pl.ylabel('Sigma H')
pl.show()


