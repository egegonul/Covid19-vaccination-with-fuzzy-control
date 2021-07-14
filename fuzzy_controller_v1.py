import numpy as np
import skfuzzy as fuzz
import skfuzzy.membership as mf

#controller for the first version of the vaccination
def fuzzy_controller_v1(vac_percent):
  #define domains
  vac_percent*=100
  percent= np.arange(0,100,1)
  delta= np.arange(-25,25,1)

  #partition sets
  #percent_low=mf.trimf(percent,[0,0,40])
  percent_low=mf.trimf(percent,[0,0,50])
  percent_med=mf.trimf(percent,[35,50,65])
  #percent_high=mf.trimf(percent,[60,100,100])
  percent_high=mf.trimf(percent,[50,100,100])

  delta_neg=mf.trimf(delta,[-25,-25,0])
  delta_nz=mf.trimf(delta,[-10,0,10])
  delta_pos=mf.trimf(delta,[0,25,25])

  #apply membership functions
  percent_low_mb=fuzz.interp_membership(percent,percent_low,vac_percent)
  percent_med_mb=fuzz.interp_membership(percent,percent_med,vac_percent)
  percent_high_mb=fuzz.interp_membership(percent,percent_high,vac_percent)

  #define rules
  rule1=np.fmin(percent_low_mb,delta_pos)
  rule2=np.fmin(percent_med_mb,delta_pos)
  rule3=np.fmin(percent_high_mb,delta_neg)

  delta_out=np.fmax(np.fmax(rule1,rule2),rule3)
  defuzz=fuzz.defuzz(delta,delta_out,'bisector')

  return defuzz/100