import sys, os
BIN = os.path.expanduser("../")
sys.path.append(BIN)

import LHC_FBCT
import LHC_BQM
import LHC_Energy
import LHC_BSRT
import lhc_log_db_query as lldb
import pickle

filln = 3859
pkl_name = 'fills_and_bmodes.pkl'

with open(pkl_name, 'rb') as fid:
    dict_fill_bmodes = pickle.load(fid)

t_start_fill = dict_fill_bmodes[filln]['t_startfill']
t_end_fill = dict_fill_bmodes[filln]['t_endfill']

varlist = []
varlist += LHC_FBCT.variable_list()
varlist += LHC_BQM.variable_list()
varlist += LHC_Energy.variable_list()
varlist += LHC_BSRT.variable_list()


lldb.dbquery(varlist, t_start_fill, t_end_fill, 'fill_%d.csv'%filln)
