import Orange
import matplotlib.pyplot as plt
# DATASET 1
names = ["Apromore-ProDrift adaptive", "Apromore-ProDrift fixed", "VDD system", "ProM-Concept Drift",
         'IPDD framework- Fixed', "Adaptive IPDD Trace by Trace"]
avranks = [4.53, 3.89, 2.78, 1.17, 4.36, 4.28]
cd = Orange.evaluation.compute_CD(avranks, 18, alpha='0.05', test='nemenyi')
print(cd)
Orange.evaluation.graph_ranks(avranks, names, cd=cd, width=8, textspace=2.5)
plt.show()

#DATASET 2
import Orange
import matplotlib.pyplot as plt
names = ["Apromore-ProDrift adaptive", "Apromore-ProDrift fixed", "VDD system", "ProM-Concept Drift", 'IPDD framework- Fixed',
         "Adaptive IPDD Trace by Trace" ]
avranks = [4.13, 4.13, 2.20 , 2.27, 4.13, 4.13 ]
cd = Orange.evaluation.compute_CD(avranks, 18, alpha='0.05', test='nemenyi')
print(cd)
Orange.evaluation.graph_ranks(avranks, names, cd=cd, width=8, textspace=2.5)
plt.show()

























        










