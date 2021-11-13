# F-score-calculating
This the code for calculating the F-score of Tools for process drift detection.
The structure of the program is divided by:
1. : funcions needed and the main code for calculating the F-score
2. Prom_F_Score_Calculator.py: this program calculates F-score from ProM Concept Drift plugin, the detected drift and the real drift must be inputted manually as def parameters
4. DATA: this file files was data for testing the program
    -data/data_5k-> Event logs with 5000 and 9 sudden drifts from ""
    -data/data_5k_teste-> sample from data_5k
    -data/data_1000-> Event logs with 0 noise, trace ordering, 1000 traces, 1 drift
    and 1 drift from ""
    -data/data_teste_sudden-> Sample from data_1000
    -data/output_apromore-> 4 examples of tested experiments at Apromore ProDrift plugin with logs of data_1000
    -data/output_apromore_5k-> 4 examples of tested experiments at Apromore ProDrift plugin with logs of data_5000
    -data/data_5k.zip-> Zipped archives of data_5k
    -data/data_teste_sudden.zip-> Zipped archives of data_teste_sudden
    -data/output_apromore.zip-> Zipped archives of data/output_apromore
    -data/output_apromore_5k.zip-> Zipped archives of data/output_apromore_5k
    Creat this directory and add the arhives .txt that are available at https://www.kaggle.com/caioraduy/output-off-vdd-experiments
    -data/VDD_output_5k
    -data/VDD_output_1000
    
   
   
