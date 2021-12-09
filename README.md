# F-score-calculating
This program calculates the F-score of Tools for process drift detection. The program structure is divided by:

1. VDD_APROMORE_F_Score_Calculator.py: This program calculates the F-Score for VDD and Apromore ProDrift plugin using the output of the tools.
The output of the tools are .txt files; we used them to read and compute the drift localization detected in the tool. We saved the name of the 
.txt files with the parameters and we used the file to compute the F-scre. The program computes all the F-Score and creates a .xlsx file with
each file's results and parameters.

We must save the output as a pattern, because the program uses the file name to obtain information:

1.1 VDD patterns:
    
    Dataset 1) log_name+'_9drifts_'+'subL'+ number_of_sub_log_used + '_sliBy'+ number_of_sliBy_used '_driftAll_vdd'+.txt
    log_name, number_of_sub_log_used, number_of_sliBy_used are string variables
    example:
          log_name= cb5k
          number_of_sub_log_used=50 
          number_of_sliBy_used=25
          file name: cb5k_9drifts_subL50_sliBy25_driftAll_vdd.txt
     
    Dataset 2) log_name+'_1drift_'+'subL'+ number_of_sub_log_used + '_sliBy'+ number_of_sliBy_used '_driftAll_vdd'+.txt
     log_name, number_of_sub_log_used, number_of_sliBy_used are string variables
     example:
          log_name= sudden_trace_noise0_1000_cb
          number_of_sub_log_used=50 
          number_of_sliBy_used=25
          file name:sudden_trace_noise0_1000_cb_1drift_subL50_sliBy25_driftAll_vdd.txt
           
1.2 Apromore patterns:   
       
     Dataset 1) 'log_'+log_name+ drift_analisys + '_ws' + window_size + '_' + windowing_type +'_apromore'.txt
       log_name, window_size, windowing_type are string variables
       example:
	      log_name= lp2.5k
	      drift_analisys= trace
	      window_size=50
	      windowing_type= fwin
              file name:log_lp2.5k_trace_ws25_fwin_apromore
	      
     Dataset 2) 
     'log_'+ drift_type_of_the_event_log +'_'+ size_of_the_event_log +'_'+ pattern_of_log + '_'+ drift_analisys + '_ws' + window_size + '_'+ windowing_type +'_' +'apromore'.txt
       size_of_the_event_log, size_of_the_event_log, pattern_of_log and window_size are string variables
       examples:
               log_name:sudden_trace_noise0_1000_cb
                        drift_type_of_the_event_log= sudden
                        size_of_the_event_log= 1000
                        pattern_of_log= cb
                window_size: 50
               windowing_type= adaptive
               file name: log_sudden_1000_cb_trace_ws50_adaptive_apromore.txt
                        
           
2.Prom_F_Score_Calculator.py: This program calculates F-score from ProM Concept Drift plugin, the detected drift and the real drift must be 
inputted manually as def parameters

3. data: This file has data for testing the program

    -data/data_5k-> Event logs with 5000 and 9 sudden drifts from "Maaradji, A., Dumas, M., La Rosa, M., Ostovar, A.: Fast and Accurate Business 
    Process Drift Detection. In: BPM 2016: Business Process Management. pp. 406–422. Springer, Cham, Innsbruck, Austria (2015)" 
    
    -data/data_5k_teste-> sample from data_5k -data/data_1000-> Event logs with 0 noise, trace ordering, 1000 traces, 1 drift and 1 drift from 
    "Ceravolo, P., Marques Tavares, G., Junior, S.B., Damiani, E.: Evaluation Goals for Online Process Mining: a Concept Drift Perspective. IEEE Trans. Serv. Comput. (2020). https://doi.org/10.1109/TSC.2020.3004532" 
    
    -data/data_teste_sudden-> Sample from data_1000 -data/output_apromore-> 4 examples of tested experiments at Apromore ProDrift plugin with 
    logs of data_1000 
    
    -data/output_apromore_5k-> 4 examples of tested experiments at Apromore ProDrift plugin with logs of data_5000 -data/data_5k.zip-> Zipped archives of data_5k 
    
    -data/data_teste_sudden.zip-> Zipped archives of data_teste_sudden -data/output_apromore.zip-> Zipped archives of data/output_apromore 
    
    -data/output_apromore_5k.zip-> Zipped archives of data/output_apromore_5k Create this directory and add the arhives .txt that are available at https://www.kaggle.com/caioraduy/output-off-vdd-experiments 
    
    -data/VDD_output_5k -data/VDD_output_1000 -data/OutputData -> The program VDD_APROMORE_F_Score_Calculator.py runs and then saves a .xlsx
    with the register as the output 


Both VDD_APROMORE_F_Score_Calculator.py and Prom_F_Score_Calculator.py have # with comments for the  better understanding of the program structure

If you have questions and doubts send a e-mail at: raduycaio@gmail.com or caio.raduy@pucpr.edu.br
  
