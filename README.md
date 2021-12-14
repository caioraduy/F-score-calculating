# F-score-calculating
This program calculates the F-score for process drift detection tools (Apromore ProDrift, VDD, and ProM Concept Drift). 
The program structure is divided by:

1. VDD_APROMORE_F_Score_Calculator.py: This program calculates the F-score for VDD and Apromore ProDrift plugin using the output of the tools.
The output of the tools are saved in .txt files using a specif name pattern. The program reads the files to identify the reported drifts, and then calculates all the F-scores and creates a .xlsx file with each file's metric and parameters.
The name of the files must follow the rules above:

1.1 VDD:
    Dataset 1) [log_name]_9drifts_subL[winsize]_sliBy[winstep]_driftAll_vdd.txt
    example:
          [log_name] = cb5k
          [winsize] = 50 
          [winstep] = 25
          file name: cb5k_9drifts_subL50_sliBy25_driftAll_vdd.txt
     
    Dataset 2) [log_name]_1drift_subL[winsize]_sliBy[winstep]_driftAll_vdd.txt
    example:
          [log_name] = sudden_trace_noise0_1000_cb
          [winsize] = 50 
          [winstep] = 25
          file name: sudden_trace_noise0_1000_cb_1drift_subL50_sliBy25_driftAll_vdd.txt
           
1.2 Apromore:
    The parameter winsize indicates the window size for the fixed approach and the initial window size for the adaptive approach.
    
    Dataset 1) log_[log_name]_trace_ws[winsize]_[approach]_apromore.txt
    example:
     	  [log_name] = lp2.5k         
          [winsize] = 50
          [approach] = fixed
          file name: log_lp2.5k_trace_ws25_fixedn_apromore.txt
	      
    Dataset 2) log_[log_name]_trace_ws[winsize]_[approach]_apromore.txt
    example:
          [log_name] = sudden_trace_noise0_1000_cb         
          [winsize] = 50
          [approach] = adaptive
          file name:log_sudden_trace_noise0_1000_cb_trace_ws50_adaptive_apromore.txt
                        
           
2.Prom_F_Score_Calculator.py: This program calculates the F-score using the detected drifts from the ProM Concept Drift plugin. The detected drifts and the real drifts must be 
manually inputted as def parameters.

3. data: This folder contains the data for testing the program

    - data/data_5k-> Event logs with 5000 and 9 sudden drifts from "Maaradji, A., Dumas, M., La Rosa, M., Ostovar, A.: Fast and Accurate Business 
    Process Drift Detection. In: BPM 2016: Business Process Management. pp. 406–422. Springer, Cham, Innsbruck, Austria (2015)" 
    
    - data/data_1000-> Event logs with 0 noise, 1000 traces, 1 sudden drift in the control-flow perspective from 
    "Ceravolo, P., Marques Tavares, G., Junior, S.B., Damiani, E.: Evaluation Goals for Online Process Mining: a Concept Drift Perspective. IEEE Trans. Serv. Comput. (2020). https://doi.org/10.1109/TSC.2020.3004532" 
    
    - data/output_apromore_dataset1 -> experiments results from Apromore ProDrift plugin with logs of data_5k
    
    - data/output_apromore_dataset2 -> experiments results from Apromore ProDrift plugin with logs of data_1000
    
    - data/output_vdd_dataset1 and data/output_vdd_dataset2 -> folders to insert the results from VDD system. Because the files are too big, they should be downloaded from Kaggle (https://www.kaggle.com/caioraduy/output-off-vdd-experiments)
    
    - data/output_data -> folder where the program saves a .xlsx file containing the calculates F-scores
        
    
Both VDD_APROMORE_F_Score_Calculator.py and Prom_F_Score_Calculator.py have # with comments for the  better understanding of the program structure

If you have questions please send an e-mail at: raduycaio@gmail.com or caio.raduy@pucpr.edu.br
  
