import time
import numpy as np
import scipy.interpolate as spint
import pylab as pl
import timber_manag3 as tm3

timb_timestamp2float= lambda time_string: time.mktime(time.strptime(time_string,'%Y-%m-%d %H:%M:%S'))

class lhc_hl:
	def __init__(self, variable_hl):
		self.hl = np.squeeze(np.float_(variable_hl.values))
		self.t_stamps = np.array(np.float_(variable_hl.t_stamps))


class lhc_fbct:
	def __init__(self,timber_variable_FBCT):
	
		if type(timber_variable_FBCT) is str:
			dict_timber = tm3.parse_timber_file(timber_variable_FBCT, verbose=True)
			timber_variable_FBCT = dict_timber[dict_timber.keys()[0]]

		self.tstamps = timber_variable_FBCT.t_stamps
		self.bint = timber_variable_FBCT.values
		self.bint = map(lambda x: np.array(map(float, x)), self.bint)
		#~ np.array(map(float, value)))
		#~ 
		self.tstamps=np.array(self.tstamps)
		self.totint=np.array(map(sum, self.bint))
		
	def nearest_older_sample(self, t_obs, flag_return_time=False):
		ind_min=np.argmin(np.abs(self.tstamps-t_obs))
		if self.tstamps[ind_min]>t_obs:
			ind_min-=1
		if flag_return_time:	
			if ind_min == -1:
				return 0.*self.bint[ind_min], -1
			else:	
				return self.bint[ind_min], self.tstamps[ind_min]
		else:
			if ind_min == -1:
				return 0.*self.bint[ind_min]
			else:	
				return self.bint[ind_min]
		
class lhc_bloss:
	def __init__(self,full_path_stable_phase):
		with open(full_path_stable_phase) as fid:
			lines=fid.readlines()


		self.filled_buckets = np.array(map(int,lines[1].split('\n')[0].split(',')[1:]))
		lines = lines[2:]
		self.tstamps = []
		self.bloss = []

		for line in lines:
			#print line
			line = line.split('\n')[0].replace(',--',',0.')
			if ',' in line:
				itemsinline = line.split(',')
				self.tstamps.append(timb_timestamp2float(itemsinline[0].split('.')[0]))
				self.bloss.append(np.array(map(float, itemsinline[1:])))
		
		self.tstamps=np.array(self.tstamps)	
		self.totloss=np.array(map(sum, self.bloss))
		self.maxloss=np.array(map(np.max, self.bloss))
		self.meanloss=np.array(map(np.mean, self.bloss))
		#self.totloss_interp = spint.interp1d(self.tstamps, self.totloss,kind='linear',
			#bounds_error=False, fill_value=0.)

	def nearest_older_sample(self, t_obs):
		ind_min=np.argmin(np.abs(self.tstamps-t_obs))
		if self.tstamps[ind_min]>t_obs:
			ind_min-=1
			
		if ind_min == -1:
			return 0.*self.bloss[ind_min]
		else:
			return self.bloss[ind_min]
			
	def closest_samples(self, t_obs_list, t_toll):
		t_acq_list = []
		bloss_list = []
		for t_obs in t_obs_list:
			ind_min=np.argmin(np.abs(self.tstamps-t_obs))
			# if self.tstamps[ind_min]>t_obs:
			# 	ind_min-=1
				

			#print abs(self.tstamps[ind_min] - t_obs)
			if abs(self.tstamps[ind_min] - t_obs) <t_toll:
				t_acq_list.append(self.tstamps[ind_min])
				bloss_list.append(self.bloss[ind_min])
		return 	t_acq_list,	bloss_list


def mean_nonzero(x):
	mask_nonzero = x>0
	if np.sum(mask_nonzero)>0:
		return np.mean(x[mask_nonzero])
	else:		
		return 0.
		
		
class lhc_filled_buckets:
	def __init__(self, timber_variable_filled_bucket):

		if type(timber_variable_filled_bucket) is str:
			dict_timber = tm3.parse_timber_file(timber_variable_filled_bucket, verbose=True)
			timber_variable_filled_bucket = dict_timber[dict_timber.keys()[0]]
		
		self.tstamps = np.array(timber_variable_filled_bucket.t_stamps)
		self.fillbuck = timber_variable_filled_bucket.values
		
		self.fillbuck = map(lambda x: np.array(map(lambda y: int(float(y)), x)), self.fillbuck)
		self.fillbuck = map(lambda x: (x-1)/10, self.fillbuck)
		self.fillbuck = map(lambda x: x[x>=0], self.fillbuck)

		self.Nbun = map(len, self.fillbuck)
		N_acq = len(self.Nbun)
		
		self.flag_filled = []
		for ii in xrange(N_acq):
			self.flag_filled.append(np.array(map(lambda x: x in self.fillbuck[ii], range(3564))))
			
		
	def nearest_older_sample(self, t_obs):
		ind_min=np.argmin(np.abs(self.tstamps-t_obs))
		if self.tstamps[ind_min]>t_obs:
			ind_min-=1
			
		if ind_min == -1:
			return 0.*self.fillbuck[ind_min]
		else:	
			return self.fillbuck[ind_min]
			
	def nearest_older_sample_flag_filled_Nbun(self, t_obs):
		ind_min=np.argmin(np.abs(self.tstamps-t_obs))
		if self.tstamps[ind_min]>t_obs:
			ind_min-=1
			
		if ind_min == -1:
			return [], 0
		else:	
			return self.flag_filled[ind_min], self.Nbun[ind_min]
			

			
			
		
class lhc_blength:
	def __init__(self,timber_variable_blength, timber_variable_filled_bucket):

		if type(timber_variable_blength) is str:
			dict_timber = tm3.parse_timber_file(timber_variable_blength, verbose=True)
			timber_variable_blength = dict_timber[dict_timber.keys()[0]]
		
		if type(timber_variable_filled_bucket) is str:
			dict_timber = tm3.parse_timber_file(timber_variable_filled_bucket, verbose=True)
			timber_variable_filled_bucket = dict_timber[dict_timber.keys()[0]]
			fillbuck_obj = lhc_filled_buckets(timber_variable_filled_bucket)
		elif isinstance(timber_variable_filled_bucket, lhc_filled_buckets):
			fillbuck_obj = timber_variable_filled_bucket 
		else:
			fillbuck_obj = lhc_filled_buckets(timber_variable_filled_bucket)
			
		
			
		self.tstamps = timber_variable_blength.t_stamps
		self.blen = []
		blen_timberstyle = timber_variable_blength.values
		blen_timberstyle = map(lambda x: np.array(map(float, x)), blen_timberstyle)
		
		
		N_acq = len(self.tstamps)
		
		for ii in xrange(N_acq):
			blen_vect = np.zeros(3564) 
			flag_filled_curr, Nbun_curr = fillbuck_obj.nearest_older_sample_flag_filled_Nbun(self.tstamps[ii])
			blen_vect[flag_filled_curr]=(blen_timberstyle[ii][:Nbun_curr])
			self.blen.append(blen_vect)
			
		self.tstamps=np.array(self.tstamps)
		self.avblen=np.array(map(mean_nonzero, self.blen))
		
		
	def nearest_older_sample(self, t_obs, flag_return_time=False):
		ind_min=np.argmin(np.abs(self.tstamps-t_obs))
		if self.tstamps[ind_min]>t_obs:
			ind_min-=1
	
		if flag_return_time:	
			if ind_min == -1:
				return 0.*self.blen[ind_min], -1
			else:	
				return self.blen[ind_min], self.tstamps[ind_min]
		else:
			if ind_min == -1:
				return 0.*self.blen[ind_min]
			else:	
				return self.blen[ind_min]

			
class lhc_energy:
	def __init__(self,timber_variable_energy):
		if type(timber_variable_energy) is str:
			dict_timber = tm3.parse_timber_file(timber_variable_energy, verbose=True)
			timber_variable_energy = dict_timber[dict_timber.keys()[0]]

		self.tstamps = timber_variable_energy.t_stamps
		self.energy = timber_variable_energy.values
		
		self.energy = map(lambda x: float(x[0]), self.energy)
	
		self.tstamps=np.array(self.tstamps)
		self.energy=np.array(self.energy)
		
	def nearest_older_sample(self, t_obs):
		ind_min=np.argmin(np.abs(self.tstamps-t_obs))
		if self.tstamps[ind_min]>t_obs:
			ind_min-=1
		return self.energy[ind_min]
	
		
