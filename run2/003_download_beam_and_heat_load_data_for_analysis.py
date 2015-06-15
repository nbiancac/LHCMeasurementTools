import lhc_log_db_query as lldb
import pickle

filln = 3820


with open('fills_and_bmodes_run2.pkl', 'rb') as fid:
	dict_fill_bmodes = pickle.load(fid)


t_start_fill = dict_fill_bmodes[filln]['t_startfill']
t_end_fill = dict_fill_bmodes[filln]['t_endfill']


varlist_beams = [\
'LHC.BCTFR.A6R4.B1:BUNCH_INTENSITY',
'LHC.BCTFR.A6R4.B2:BUNCH_INTENSITY', \
'LHC.BQM.B1:FILLED_BUCKETS', \
'LHC.BQM.B2:FILLED_BUCKETS', \
'LHC.BQM.B1:BUNCH_LENGTHS', \
'LHC.BQM.B2:BUNCH_LENGTHS',
'LHC.BSRA.US45.B2:ABORT_GAP_ENERGY']

lldb.dbquery(varlist_beams, t_start_fill, t_end_fill, 'fill%d_beams.csv'%filln)

varlist_QBS_ITs_and_some_SAMs = [\
'QBS_D3L4',
'QBS_ITL1',
'QBS_ITL2',
'QBS_ITL5',
'QBS_ITL8',
'QBS_ITR1',
'QBS_ITR2',
'QBS_ITR5',
'QBS_ITR8',
'QBS_Q5L1',
'QBS_Q5L5',
'QBS_Q5R1',
'QBS_Q5R5',
'QBS_Q6L1',
'QBS_Q6L5',
'QBS_Q6R1',
'QBS_Q6R5']
lldb.dbquery(varlist_QBS_ITs_and_some_SAMs, t_start_fill, t_end_fill, 'fill%d_ITs_and_some_SAMs.csv'%filln)


print "!!!!!!!!!!!!1WARNING All corrections from the database have been removed!!!!!!"
