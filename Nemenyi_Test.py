import Orange
import matplotlib.pyplot as plt
# DATASET 1
names = ["Apromore-ProDrift adaptive", "Apromore-ProDrift fixed", "VDD system", "ProM-Concept Drift",
         'IPDD framework- Fixed', "Adaptive IPDD Trace by Trace"]
avranks = [4.53, 4.53, 2.77, 2.4, 2.23, 4.53]
cd = Orange.evaluation.compute_CD(avranks, 18, alpha='0.05', test='nemenyi')
print(cd)
Orange.evaluation.graph_ranks(avranks, names, cd=cd, width=8, textspace=2.5)
plt.show()

#DATASET 2
import Orange
import matplotlib.pyplot as plt
names = ["Apromore-ProDrift adaptive", "Apromore-ProDrift fixed", "VDD system", "ProM-Concept Drift", 'IPDD framework- Fixed',
         "Adaptive IPDD Trace by Trace" ]
avranks = [4.28, 4.94, 3.61, 1.25, 2.22, 4.69 ]
cd = Orange.evaluation.compute_CD(avranks, 18, alpha='0.05', test='nemenyi')
print(cd)
Orange.evaluation.graph_ranks(avranks, names, cd=cd, width=8, textspace=2.5)
plt.show()

























        










