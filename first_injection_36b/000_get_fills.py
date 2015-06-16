import sys, os
BIN = os.path.expanduser("../")
sys.path.append(BIN)

import lhc_log_db_query as lldb
import TimestampHelpers as th
import LHC_Fills

# t_start_string = '2015_06_14 19:30:00'
t_start_string = '2015_06_14 15:30:00'
t_stop_string = '2015_06_14 21:30:00'

t_start = th.localtime2unixstamp(t_start_string)
t_stop = th.localtime2unixstamp(t_stop_string)

filename = 'fills_and_bmodes'
csv_name = filename + '.csv'
pkl_name = filename + '.pkl'

# Get data from database
varlist = LHC_Fills.get_varlist()
lldb.dbquery(varlist, t_start, t_stop, csv_name)

# Make pickle
LHC_Fills.make_pickle(csvname, pkl_name)

