from vaccination import Vaccination
from fuzzy_controller_v1 import fuzzy_controller_v1
from fuzzy_controller_v2 import fuzzy_controller_v2


#simulation loop for the first version of the vaccine
vac= Vaccination()
cost=0
for iteration in range(200):
  vac_percent,dummy=vac.checkVaccinationStatus()
  #print("vac_percent= ", vac_percent)
  delta=fuzzy_controller_v1(vac_percent)
  #print("delta= ",delta)
  vac.vaccinatePeople(delta)
  if(iteration<90):
    cost+=vac.vaccinated_percentage_curve_[-1]
print(vac.vaccinated_percentage_curve_[-1])

#simulation for the second loop of the vaccine
vac_v2= Vaccination()
cost_v2=0
for iteration in range(200):
  vac_v2_percent,vac_v2_rate=vac_v2.checkVaccinationStatus()
  #print("vac_percent= ", vac_v2_percent,"vac_rate= ",vac_v2_rate)
  delta=fuzzy_controller_v2(vac_v2_percent,vac_v2_rate)
  #print("delta= ",delta)
  vac_v2.vaccinatePeople(delta)
  if(iteration<110):
    cost_v2+=vac.vaccinated_percentage_curve_[-1]
print(vac_v2.vaccinated_percentage_curve_[-1])






