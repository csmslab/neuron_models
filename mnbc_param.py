"""
Created on Fri May 22 10:13:01 2015
@author: vigil
"""

# Script parameters

#display_timespan = 2000

# Units

s = 1
ms = s/1000
us = ms/1000

C = 1
V = 1

F = C/V
mF = F/1000
uF = mF/1000
nF = uF/1000
pF = nF/1000
fF = pF/1000

# Global parameters

C_m = 2*pF 		# Membrane capacitance
C_l = 20*fF 	# Leakage capacitance
#V_r_m = 1*V 	# Membrane rest potential
#V_r_t = 3*V 	# Threshold rest potential

Update_mode = 'discrete' # continuous or discrete

# Model parameters
	# timespan 	- Simulation duration in us
	# f_l_m 	- Membrane capacitor switching frequency
	# f_l_t 	- Threshold capacitor switching frequency
	# C_s_m 	- Membrane switching capacitor
	# C_s_t 	- Threshold swithing capacitor
	# E_m 	- Equivalent voltage of Iext
	#	 	 	key is index 0, 1, ....
	#	 	 	tuple[0] is time instant
	# 	 	 	tuple[1] is voltage

# Membrane capacitances
# W4+W3+W2+W1+W0 = 155 fF
# W4+W3+W2+W1    = 150 fF
# W4+W3+W2       = 140 fF
# W4+W3          = 120 fF
# W4             = 80 fF
# W3+W2+W1+W0    = 75 fF
# W3+W2+W1       = 70 fF
# W3+W2          = 60 fF
# W3             = 40 fF
# W2+W1+W0       = 35 fF
# W2+W1          = 30 fF
# W2             = 20 fF
# W1+W0          = 15 fF
# W1             = 10 fF
# W0             = 5 fF

#E_m_pseudo -> E_m for plotting 0 to 5 = -2 to -1
neuron_behavior_params =	{'Tonic spiking': 	{'timespan'	: 600, #1000,
									 'f_l_m'   	: 10000/s, #10000/s,
									 'f_l_t'   	: 200000/s,
									 'C_s_m' 	: 175*fF,
								       'C_s_t'	: 0*fF,
									 'V_r_m'   : 1*V,
									 'V_r_t'   : 4*V,
						                  'E_m'	: {0 : (0, 0*V),
									              1 : (20, 5*V),
									              2 : (1000, 5*V)}
					},
					'Phasic spiking': 	{'timespan'	: 700, #2000,
									 'f_l_m'   	: 3000000/s,
									 'f_l_t'   	: 200/s,
									 'C_s_m' 	: 175*fF,
								       'C_s_t'	: 30*fF,
									 'V_r_m'   : 1*V,
									 'V_r_t'   : 3*V,
						                  'E_m'	: {0 : (0, 0*V),
									              1 : (20, 5*V),
									              2 : (2000, 5*V)}
					},
					'Spike frequency adaptation': 	{'timespan'	: 1200, #2000,
									 'f_l_m'   	: 10000/s,
									 'f_l_t'   	: 200000/s,  #200000/s,
									 'C_s_m' 	: 175*fF,
								       'C_s_t'	: 30*fF,
									 'V_r_m'   : 1*V,
									 'V_r_t'   : 3*V,
						                  'E_m'	: {0 : (0, 0*V),
									              1 : (20, 5*V),
									              2 : (2000, 5*V)}
					},
#					'Accomodation':	 	{'timespan'	: 3000, #3000,
#									 'f_l_m'   	: 1000000/s,
#									 'f_l_t'   	: 3000000/s,
#									 'C_s_m' 	: 175*fF,
#								       'C_s_t'	: 75*fF,
#									 'V_r_m'   : 1*V,
#									 'V_r_t'   : 2.7*V,
#						                  'E_m'	: {0 : (0, 1*V),
#									              1 : (100, 5*V),
#									              2 : (250, 1*V), # V_r_m
#		                                                      3 : (2000, 2.3*V),
#									              4 : (2150, 3.6*V),
#									              5 : (2300, 5*V),
#                                                                 6 : (2450, 1*V), # V_r_m
#									              7 : (3000, 1*V)} # V_r_m
#					},
					'Accomodation':	 	{'timespan'	: 18000, #3000,
									 'f_l_m'   	: 1000000/s,
									 'f_l_t'   	: 3000000/s,
									 'C_s_m' 	: 175*fF,
								       'C_s_t'	: 75*fF,
									 'V_r_m'   : 1*V,
									 'V_r_t'   : 2.7*V,
						                  'E_m'	: {0 : (0, 1*V),
									              1 : (100, 5*V),
									              2 : (250, 1*V), # V_r_m
		                                                      3 : (800, 2.3*V),
									              4 : (950, 3.6*V),
									              5 : (1100, 5*V),
                                                                 6 : (1250, 1*V), # V_r_m
									              7 : (1800, 1*V)} # V_r_m
					},
#					'Integrator': 	{'timespan'	: 3000,
#									 'f_l_m'   	: 100000/s,
#									 'f_l_t'   	: 3000000/s,
#									 'C_s_m' 	: 175*fF,
#								       'C_s_t'	: 20*fF,
#									 'V_r_m'   : 1*V,
#									 'V_r_t'   : 3.3*V,
#						                  'E_m'	: {0 : (0, 1*V), # V_r_m
#									              1 : (100, 5*V),
#									              2 : (200, 1*V), # V_r_m
#										        3 : (300, 5*V),
#										        4 : (400, 1*V),
#										        5 : (2000, 1*V),
#										        6 : (2100, 5*V),
#										        7 : (2200, 1*V),
#										        8 : (2400, 5*V),
#										        9 : (2500, 1*V),
#                                                                 10 : (3000, 1*V)} # V_r_m
#					},
					'Integrator': 	{'timespan'	: 1400,
									 'f_l_m'   	: 100000/s,
									 'f_l_t'   	: 3000000/s,
									 'C_s_m' 	: 175*fF,
								       'C_s_t'	: 20*fF,
									 'V_r_m'   : 1*V,
									 'V_r_t'   : 3.3*V,
						                  'E_m'	: {0 : (0, 1*V), # V_r_m
									              1 : (100, 5*V),
									              2 : (200, 1*V), # V_r_m
										        3 : (300, 5*V),
										        4 : (400, 1*V),
										        5 : (600, 1*V),
										        6 : (700, 5*V),
										        7 : (800, 1*V),
										        8 : (1000, 5*V),
										        9 : (1100, 1*V),
                                                                 10 : (1400, 1*V)} # V_r_m
					},
#					'Threshold variability':	 	{'timespan'	: 3000,
#									 'f_l_m'   	: 10000/s,
#									 'f_l_t'   	: 300000/s,
#									 'C_s_m' 	: 175*fF,
#								       'C_s_t'	: 75*fF,
#									 'V_r_m'   : 2*V,
#									 'V_r_t'   : 4*V,
#						                  'E_m'	: {0 : (0, 2*V),
#									              1 : (100, 5*V),
#									              2 : (300, 2*V), # V_r_m
#		                                                      3 : (2000, 0*V),
#									              4 : (2200, 2*V), # V_r_m
#									              5 : (2400, 5*V),
#                                                                 6 : (2600, 2*V), # V_r_m
#									              7 : (3000, 2*V)} # V_r_m
#					},
					'Threshold variability':	 	{'timespan'	: 2500,
									 'f_l_m'   	: 10000/s,
									 'f_l_t'   	: 300000/s,
									 'C_s_m' 	: 175*fF,
								       'C_s_t'	: 75*fF,
									 'V_r_m'   : 2*V,
									 'V_r_t'   : 4*V,
						                  'E_m'	: {0 : (0, 2*V),
									              1 : (100, 5*V),
									              2 : (300, 2*V), # V_r_m
		                                                      3 : (1600, 0*V),
									              4 : (1800, 2*V), # V_r_m
									              5 : (2000, 5*V),
                                                                 6 : (2200, 2*V), # V_r_m
									              7 : (2500, 2*V)} # V_r_m
					},
#					'Rebound spike': 		{'timespan'	: 1000,
#									 'f_l_m'   	: 10000/s,
#									 'f_l_t'   	: 30000/s,
#									 'C_s_m' 	: 175*fF,
#								       'C_s_t'	: 60*fF,
#									 'V_r_m'   : 2*V,
#									 'V_r_t'   : 4*V,
#						                  'E_m'	: {0 : (0, 2*V),
#									              1 : (100, 0*V),
#									              2 : (800, 2*V), # V_r_m
#										        3 : (1000, 0*V)} # V_r_m
#                          },
					'Rebound spike': 		{'timespan'	: 800,
									 'f_l_m'   	: 10000/s,
									 'f_l_t'   	: 30000/s,
									 'C_s_m' 	: 175*fF,
								       'C_s_t'	: 60*fF,
									 'V_r_m'   : 2*V,
									 'V_r_t'   : 4*V,
						                  'E_m'	: {0 : (0, 2*V),
									              1 : (100, 0*V),
									              2 : (600, 2*V), # V_r_m
										        3 : (800, 0*V)} # V_r_m
					},
					'Input bistability': 	{'timespan'	: 800, # 1000
									 'f_l_m'   	: 10000/s,
									 'f_l_t'   	: 30000/s,
									 'C_s_m' 	: 175*fF,
								       'C_s_t'	: 20*fF,
									 'V_r_m'   : 1*V,
									 'V_r_t'   : 3*V,
						                  'E_m'	: {0 : (0, 1*V), # V_r_m
									              1 : (100, 4*V),
									              2 : (500, 1*V), # V_r_m
										        3 : (600, 4*V),
                                                                 4 : (800, 1*V)} # V_r_m    # 1000
#										        {0 : (0, 1*V), # V_r_m
#									              1 : (100, 4*V),
#									              2 : (120, 1*V), # V_r_m
#										        3 : (600, 4*V),
#										        4 : (620, 1*V),
#                                                                5 : (1000, 1*V)} # V_r_m
					},
					'Class 1': 			{'timespan'	: 1600, # 3000
									 'f_l_m'   	: 1/s,
									 'f_l_t'   	: 300/s,
									 'C_s_m' 	: 175*fF,
								       'C_s_t'	: 0*fF,
									 'V_r_m'   : 1*V,
									 'V_r_t'   : 3.5*V,
						                  'E_m'	: {0 : (0, 0*V),
									              1 : (100, 3.51*V),
									              2 : (3000, 3.51*V)}
#					'Class 1': 			{'timespan'	: 3000,
#									 'f_l_m'   	: 1/s,
#									 'f_l_t'   	: 30000/s,
#									 'C_s_m' 	: 175*fF,
#								       'C_s_t'	: 0*fF,
#									 'V_r_m'   : 1.0*V,
#									 'V_r_t'   : 2.5*V,
#						                  'E_m'	: {0 : (0, 0*V),
#									              1 : (100, 2.51*V),
#											2 : (1000, 3.51*V),
#											3 : (2000, 4.51*V),
#									              4 : (3000, 4.51*V)}
					},
					'Hyperpolarization induced spiking': 	{'timespan'	: 1000,
									 'f_l_m'   	: 10000/s,
									 'f_l_t'   	: 3000/s,
									 'C_s_m' 	: 175*fF,
								       'C_s_t'	: 100*fF,
									 'V_r_m'   : 2*V,
									 'V_r_t'   : 3*V,
						                  'E_m'	: {0 : (0, 2*V), # V_r_m
									              1 : (100, 0*V),
									              2 : (1000, 0*V)}
					},
			}
