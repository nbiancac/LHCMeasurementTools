from scipy.constants import c
import numpy as np

def compute_luminosity(N_colliding_bunches, ppb, bunch_length_4sigma_s, nemitt_tr, energy_eV, betastar, crossing_angle_full_rad):

	frev = 11245.
	mass_proton_eV = 938e6
	
	gamma_rel = energy_eV/mass_proton_eV

	sigma_xy = np.sqrt(betastar*nemitt_tr/gamma_rel)
	sigma_z = bunch_length_4sigma_s/4.*c

	luminosity_Hz_cm2 = 1e-4*N_colliding_bunches*ppb**2*frev/(4*np.pi*sigma_xy**2)/np.sqrt(1.+(sigma_z/sigma_xy*crossing_angle_full_rad/2)**2)

	return luminosity_Hz_cm2
