# F-score-calculating
This program calculates the F-score for process drift detection tools (Apromore ProDrift, VDD, and ProM Concept Drift). 
The program structure is divided by:

1. F_Score_Calculator.py: This program calculates the F-score for VDD and Apromore ProDrift plugin using the output of the tools. The output of the tools are saved in .txt files using a specific name pattern. The program reads the files to identify the reported drifts, and then calculates all the F-scores. For the ProM Concept Drift plugin, the drifts are reported in a png file. In this case the reported drifts are manually inputted in the program. After calculating all the F-scores the program saves an .xlsx file with each file's metric and the parameters.
For VDD and Apromore ProDrift the files must follow the rules described bellow:

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
1.3 IPDD:
     Dataset 1) IPDD_[log_name]_ws[winsize]_[approach].txt (Trace by trace)
     example:
     		[log_name] = cb5k
		[winsize] = 50 
                [approach] = fixed 
                file name: IPDD_cb5k_ws50_fixed.txt
           
3. data: This folder contains the data from the performed scenarios

    - data/data_5k-> Event logs with 5000 and 9 sudden drifts from "Maaradji, A., Dumas, M., La Rosa, M., Ostovar, A.: Fast and Accurate Business 
    Process Drift Detection. In: BPM 2016: Business Process Management. pp. 406–422. Springer, Cham, Innsbruck, Austria (2015)" 
    
    - data/data_1000-> Event logs with 0 noise, 1000 traces, 1 sudden drift in the control-flow perspective from 
    "Ceravolo, P., Marques Tavares, G., Junior, S.B., Damiani, E.: Evaluation Goals for Online Process Mining: a Concept Drift Perspective. IEEE Trans. Serv. Comput. (2020). https://doi.org/10.1109/TSC.2020.3004532" 
    
    - data/output_apromore_dataset1 -> experiments results from Apromore ProDrift plugin with logs of data_5k
    
    - data/output_apromore_dataset2 -> experiments results from Apromore ProDrift plugin with logs of data_1000
    
    - data/output_vdd_dataset1 and data/output_vdd_dataset2 -> folders to insert the results from VDD system. Because the files are too big, they should be downloaded from Kaggle (https://www.kaggle.com/caioraduy/output-vdd-dataset1-and-dataset2)
	
	- data/output_ProM_dataset1 and data/output_ProM_dataset2 contains the plots from the performed experiments using ProM Concept Drift plugin. By the time we performed the experiments we only can execute the adaptive approach with local features. 
    
    - data/output_data -> folder where the program saves the .xlsx file containing the calculates F-scores
        
    
If you have questions please send an e-mail at: raduycaio@gmail.com or caio.raduy@pucpr.edu.br
  
