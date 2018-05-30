# -*- coding: utf-8 -*-
"""
Created on Fri May 22 10:14:37 2015
@author: vigil
Mihalas-Niebur-Brandli-Cummings Neuron Model
"""
from mnbc_param import *
from numpy import zeros
from matplotlib.pyplot import plot, legend, ylim, title, xlim, show
import seaborn
seaborn.set_style('whitegrid')

#seaborn.set_style('ticks')
#seaborn.despine()

ACTUAL_MIN_VALUE = 0
ACTUAL_MAX_VALUE = 5
SCALE_MIN_VALUE = -2
SCALE_MAX_VALUE = -1

def scale_value(actual_value, actual_min_value, actual_max_value, scale_min_value, scale_max_value):
	scaled_value = (((scale_max_value - scale_min_value)*(actual_value - actual_min_value))/(actual_max_value - actual_min_value)) + scale_min_value
	return scaled_value

def MNBC_Neuron_Model(neuron_behavior, threshold_mode):
	""" Mihalas-Niebur-Brandli-Cummings Neuron Model
	neuron_behavior -> one of the many behaviors mentioned in the
				  Parameters.py file
	threshold_mode 	 	    -> static or dynamic threshold mode
	run_mode 	 	 	    -> continuous or discrete 	 - add later
	"""
	timespan = neuron_behavior_params[neuron_behavior]['timespan']
	f_l_m    = neuron_behavior_params[neuron_behavior]['f_l_m']
	f_l_t    = neuron_behavior_params[neuron_behavior]['f_l_t']
	C_s_m    = neuron_behavior_params[neuron_behavior]['C_s_m']
	C_s_t    = neuron_behavior_params[neuron_behavior]['C_s_t']
	V_r_m    = neuron_behavior_params[neuron_behavior]['V_r_m']
	V_r_t    = neuron_behavior_params[neuron_behavior]['V_r_t']
	E_m_dict    = neuron_behavior_params[neuron_behavior]['E_m']

	# Initialize arrays
	V_m = zeros(timespan)
	V_t = zeros(timespan)
	E_m = zeros(timespan)
	spike = zeros(timespan)
	E_m_pseudo = zeros(timespan)

	# Initialize membrane, threshold voltages and E_m values
	V_m[0] = V_r_m
	V_t[0] = V_r_t
	E_m[0] = E_m_dict[0][1]
	E_m_pseudo[0] = SCALE_MIN_VALUE
	spike[0] = -5

	for t in range(1, timespan):

		# Neuron membrane potential leakage
		dV_m = (1/C_m) * f_l_m * C_l * (V_r_m - V_m[t-1])
		V_m[t] = V_m[t-1] + dV_m * us

		# Generating E_m (Same as Iext, but voltage)
		length_E_m_dict = len(E_m_dict)
		for index in range(1, length_E_m_dict):
			if E_m_dict[index-1][0] < t <= E_m_dict[index][0] :
				E_m[t] = E_m_dict[index-1][1]
				E_m_pseudo[t] = scale_value(E_m_dict[index-1][1], ACTUAL_MIN_VALUE, ACTUAL_MAX_VALUE, SCALE_MIN_VALUE, SCALE_MAX_VALUE ) # scaling E_m to -3 to -2 for 0 to 5

		# Neuron membrane potential with input spike
		dV_m = (1/C_m) * C_s_m * (E_m[t] - V_m[t])

		# Continuous or discrete membrane voltage update
		if (Update_mode == 'continuous'):
			V_m[t] = V_m[t] + dV_m
		else:
			if (t % 10 == 0):		# In discrete mode membrane gets updated at every 10us
				V_m[t] = V_m[t] + dV_m
			else:
				V_m[t] = V_m[t-1]

		if (threshold_mode == 'static') :	# Determine mode
			# Static threshold
			V_t[t] = V_r_t
		else:
			# Threshold leakage
			dV_t = (1/C_m) * f_l_t * C_l * (V_r_t - V_t[t-1])
			V_t[t] = V_t[t-1] + dV_t * us

			# Threshold variation with input spike
			dV_t = (1/C_m) * C_s_t * (V_m[t] - V_r_m)

			# Continuous or discrete threshold voltage update
			if (Update_mode == 'continuous'):
				V_t[t] = V_t[t] + dV_t
			else:
				if (t % 10 == 0):		# In discrete mode threshold gets updated at every 10us
					V_t[t] = V_t[t] + dV_t
				else:
					V_t[t] = V_t[t-1]


		# Clamp threshold voltage to voltage rail
		if V_t[t] > 5:
			V_t[t] = 5

		# Spike generation
		if V_m[t] > V_t[t] :
			spike[t] = V_m[t-1]
			V_m[t-1] = V_t[t]
			V_m[t] = V_r_m
			#spike[t] = 5
			# Reset threshold potential
			if V_m[t] > V_t[t]:
				V_t[t] = V_r_t
		else:
			spike[t] = -5

	return timespan, E_m, V_m, V_t, spike, E_m_pseudo


if __name__ == '__main__' :
	Neuron_behavior = 'Accomodation'
	[timespan, E_m, V_m, V_t, spike, E_m_pseudo] = MNBC_Neuron_Model(Neuron_behavior, 'dynamic')
	time = range(timespan)
	display_timespan = timespan
	plot(time[:display_timespan], E_m_pseudo[:display_timespan],
		time[:display_timespan], V_m[:display_timespan],
		time[:display_timespan], V_t[:display_timespan],
		time[:display_timespan], spike[:display_timespan])

	legend(['E_m', 'V_m', 'V_t', 'spike'])
	title(Neuron_behavior)
	ylim([-3, 6])
	show()
