# F-score-calculating
This program calculates the F-score of Tools for process drift detection. The structure of the program is divided by:

1.VDD_APROMORE_F_Score_Calculator.py: This program calculates the F-Score for VDD and Apromore ProDrift plugin using the output of the tools. The output of the tools are .txt files; we used them to read and compute the drift localization detected in the tool. We saved the name of the .txt files with the parameters and we used the file to compute the F-scre. The program computes all the F-Score and creates a .xlsx file with each file's results and parameters.
2.Prom_F_Score_Calculator.py: This program calculates F-score from ProM Concept Drift plugin, the detected drift and the real drift must be inputted manually as def parameters
3.data: This file has data for testing the program 
    -data/data_5k-> Event logs with 5000 and 9 sudden drifts from "Maaradji, A., Dumas, M., La Rosa, M., Ostovar, A.: Fast and Accurate Business Process Drift Detection. In: BPM 2016: Business Process Management. pp. 406–422. Springer, Cham, Innsbruck, Austria (2015)" 
    -data/data_5k_teste-> sample from data_5k -data/data_1000-> Event logs with 0 noise, trace ordering, 1000 traces, 1 drift and 1 drift from "" 
    -data/data_teste_sudden-> Sample from data_1000 -data/output_apromore-> 4 examples of tested experiments at Apromore ProDrift plugin with logs of data_1000 
    -data/output_apromore_5k-> 4 examples of tested experiments at Apromore ProDrift plugin with logs of data_5000 -data/data_5k.zip-> Zipped archives of data_5k 
    -data/data_teste_sudden.zip-> Zipped archives of data_teste_sudden -data/output_apromore.zip-> Zipped archives of data/output_apromore 
    -data/output_apromore_5k.zip-> Zipped archives of data/output_apromore_5k Create this directory and add the arhives .txt that are available at https://www.kaggle.com/caioraduy/output-off-vdd-experiments 
    -data/VDD_output_5k -data/VDD_output_1000 -data/OutputData -> The program VDD_APROMORE_F_Score_Calculator.py runs and then saves a .xlsx with the register as the output 


Both VDD_APROMORE_F_Score_Calculator.py and Prom_F_Score_Calculator.py have # with comments for the  better understanding of the program structure
  
