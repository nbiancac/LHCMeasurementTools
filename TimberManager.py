import time
from numpy import float_
import numpy as np
import calendar
import os

timb_timestamp2float= lambda time_string: time.mktime(time.strptime(time_string,'%Y-%m-%d %H:%M:%S'))
timb_timestamp2float_UTC= lambda time_string: calendar.timegm(time.strptime(time_string,'%Y-%m-%d %H:%M:%S'))

def UnixTimeStamp2UTCTimberTimeString(t):
	return time.strftime('%Y-%m-%d %H:%M:%S.000', time.gmtime(t))

class timber_data_line:
	def __init__(self, rline, time_input_UTC = False):
		list_values = rline.split(',')
		t_string = list_values[0]
		if time_input_UTC:
			self.timestamp = timb_timestamp2float_UTC(t_string.split('.')[0])
			self.ms = float(t_string.split('.')[-1])
		else:
			self.timestamp = timb_timestamp2float(t_string.split('.')[0])
			self.ms = float(t_string.split('.')[-1])
		self.data_strings = list_values[1:]
                
		
class timber_variable_list:
	def __init__(self):
		self.t_stamps = []
		self.ms = []
		self.t_str=[]
		self.values = []
	def float_values(self):
		return np.squeeze(np.float_(self.values))

def parse_timber_file(timber_filename, verbose=True):

	with open(timber_filename) as fid:
		timber_lines = fid.readlines()
		
	time_input_UTC = False

	N_lines = len(timber_lines)

	i_ln = 0

	variables = {}
	while i_ln < N_lines:
		line = timber_lines[i_ln]
		line = line.split('\n')[0]
		i_ln = i_ln + 1
		
		if 'VARIABLE:' in line:
			vname = line.split(': ')[-1]
			if verbose:
				print '\n\nStarting variable: ' + vname
			variables[vname] = timber_variable_list()
		else:
			try:
				currline_obj = timber_data_line(line, time_input_UTC=time_input_UTC)
                                if currline_obj.data_strings == ['']:
                                        raise ValueError
				variables[vname].t_stamps.append(currline_obj.timestamp)
				variables[vname].values.append(currline_obj.data_strings)
				variables[vname].ms.append(currline_obj.ms)
			except ValueError:
				if 'Timestamp (UTC_TIME)' in line:
					time_input_UTC = True
					if verbose: print 'Set time to UTC'
				if verbose:
					print 'Skipped line: '+	line
					
	return variables
	
def timber_variables_from_h5(filename):
	import h5py
	dict_data = {}
	with h5py.File(filename, 'r') as fid:
		for kk in fid.keys():
			varname = kk.split('!')[0]
			part = kk.split('!')[1]
			if varname not in dict_data:
				dict_data[str(varname)] = timber_variable_list()
			if part=='t_stamps':
				dict_data[varname].t_stamps =  np.atleast_1d(fid[kk][:])
			elif part=='values':
				dict_data[varname].values =  list(np.atleast_2d(fid[kk][:]))
			
	return dict_data

	
	


def dbquery(varlist, t_start, t_stop,step=None,filename='dummy'):
	
	if type(t_start) is not str:
		t_start_str_UTC = UnixTimeStamp2UTCTimberTimeString(t_start)
	else:
		t_start_str_UTC = t_start
		
	if type(t_stop) is not str:
		t_stop_str_UTC = UnixTimeStamp2UTCTimberTimeString(t_stop)
	else:
		t_stop_str_UTC = t_stop	
	

	
	if type(varlist) is not list:
		raise TypeError
		
	varlist_str = ''
	for var in varlist:
		varlist_str += var +','
	varlist_str = varlist_str[:-1]
	
	if step:
		NI,IT=step.split()
		if IT in ['SECOND','MINUTE', 'HOUR','WEEK','MONTH','YEAR']:
			step_interval=' -IT "'+IT+'" -NI "'+NI+'" '
	else:
		step_interval=''
	execut = 'java -jar accsoft-cals-extractor-client-nodep.jar '
	config = ' -C mdb_UTC.conf '
	time_interval = ' -t1 "'+ t_start_str_UTC +'" -t2 "'+ t_stop_str_UTC +'"' 
	variables = '-vs "%s"'%(varlist_str)
	outpfile = ' -N .//' + filename

	command = execut + config + variables + time_interval + step_interval + outpfile 

	print command
	
	os.system(command)
	


	


	




		
	
	

