import os



def dbquery(varlist, t_start_str_UTC, t_stop_str_UTC, filename):
	execut = 'java -jar accsoft-cals-extractor-client-nodep.jar '
	config = ' -C ldb_UTC.conf '
	time_interval = ' -t1 "'+ t_start_str_UTC +'" -t2 "'+t_stop_str_UTC+'"' 
	variables = '-vs "%s"'%(varlist)
	outpfile = ' -N .//'+filename

	command = execut+config+variables+time_interval+outpfile

	os.system(command)
	
	
filename_test = 'test.csv'

t_start_str_UTC_test  = '2015-06-03 07:00:00.000'
t_stop_str_UTC_test  ='2015-06-04 07:00:00.000'

varlist_test = 'LHC.BCTFR.A6R4.B1:BEAM_INTENSITY'
	
dbquery(varlist_test, t_start_str_UTC_test, t_stop_str_UTC_test, filename_test)
