import lhc_log_db_query as lldb

filename = 'fills_and_bmodes_run2.csv'

t_start_str_UTC  = '2015-06-03 07:00:00.000'
t_stop_str_UTC  ='2015-06-04 07:00:00.000'

varlist = ['HX:BMODE_ABORT',
 'HX:BMODE_SQUEEZE',
 'HX:BMODE_PRERAMP',
 'HX:BMODE_SETUP',
 'HX:BMODE_WBDUMP',
 'HX:BMODE_NOMODE',
 'HX:BMODE',
 'HX:BMODE_ADJUST',
 'HX:FILLN',
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
 
 
print 'Dont worry, it takes about 10min but it works :-)'
lldb.dbquery(varlist, t_start_str_UTC, t_stop_str_UTC, filename)
