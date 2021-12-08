import pm4py
import pandas as pd
import os

# This is one of the most important function of the program,
# it uses the TP, FP, FN for
# calculating the F-score
def F_score_calcule(detected_drifts_list, win_size, number_of_real_drift_dataset,
                    real_drifts_detected):
    error_tolerance = int(win_size)
    number_of_real_drifts = number_of_real_drift_dataset

    if number_of_real_drift_dataset == 9:
        real_drifts = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
    elif number_of_real_drift_dataset == 1:
        real_drifts = [500]
    else:
        real_drifts= real_drifts_detected


    detected_drifts_list = detected_drifts_list

    real_drifts.sort()
    tp = []
    fp = []
    # here we compare the drifts detected and add the TP or FP
    for x in range(0, len(detected_drifts_list)):
        for y in range(0, len(real_drifts)):
            TP_found = False
            dist = detected_drifts_list[x] - real_drifts[y]
            # we only consider the drift detected as TP, if the drift is detected after
            # the real drift and the error tolerance is lower than the window size
            if dist >= 0 and dist <= error_tolerance:
                tp.append(dist)
                TP_found = True
                real_drifts.remove(real_drifts[y])
                break
        if not TP_found:
            fp.append(dist)
    TP = len(tp)
    FP = len(fp)
    FN = number_of_real_drifts - TP
    f_score = TP / (TP + (FP + FN) / 2)

    return f_score

#This function calculates real drifts of the base with 5000 trace and 9 drifts
def calculates_real_drift_when_analyzing_dataset1_as_event_stream(log, event_stream):
    list_with_trace_identifier = []
    for i in range(500, 5000, 500):
        x = log[i].attributes['concept:name']
        list_with_trace_identifier.append(x)
    real_drift_index_when_reading_as_event_stream = []
    for x in list_with_trace_identifier:
        for i, item in enumerate(event_stream):
            if item['case:concept:name'] == x:
                real_drift_index_when_reading_as_event_stream.append(i)
                break
    return real_drift_index_when_reading_as_event_stream

#This function calculates real drifts of the base with 1000 trace and 1 drifts, when reading
# the file as an event stream
def calcula_drift_reais_analise_events_sudden_1000(log, event_stream):
    real_drift = log[500].attributes['concept:name']
    for i, item in enumerate(event_stream):
        if item['case:concept:name'] == real_drift:
            real_drift_index_when_reading_as_event_stream = i
            break
    return real_drift_index_when_reading_as_event_stream

#this function extracts the information of the file with the output of ProDrift Plugin
def extracts_information_from_dataset1_apromore_file(file_name):
    file_name_being_analyzed = file_name
    splitline = file_name_being_analyzed.split('_')
    windowing_type = splitline[6]
    approach = splitline[4]
    tool = 'apromore'
    log_name = splitline[1] + ' ' + splitline[2] + ' ' + splitline[3]
    windows_size = splitline[5]
    windows_size = windows_size[2:]
    if windows_size == 'default':
        windows_size = 200
    else:
        windows_size = int(float(windows_size))

    return tool, log_name, approach, windowing_type, windows_size

#this function extracts information from the archive of the bases with 1000 and 1 drift a VDD
def extracts_information_from_dataset2_VDD_file(file_name):
    file_name_being_analyzed = file_name
    splitline = file_name_being_analyzed.split('_')
    windowing_type = 'fixed'
    approach = splitline[1]
    log_name = splitline[0] + ' ' + splitline[3] + ' ' + splitline[4]
    windows_size = splitline[6]
    windows_size = int(windows_size[4:])
    tool = splitline[9]
    tool = tool[:-4]
    win_step = splitline[7]
    win_step = int(win_step[5:])

    return tool, log_name, approach, windowing_type, windows_size, win_step

#this funcion extracts information of the archives .txt for the event logs
# with 9 drift and 5000 traces for Apromore
def extracts_information_from_dataset1_Apromore_file(file_name):
    file_name_being_analyzed = file_name
    splitline = file_name_being_analyzed.split('_')
    log_name = splitline[1]
    approach = splitline[2]
    windows_size = splitline[3]
    windows_size = windows_size[2:]
    if windows_size == 'default':
        windows_size = 200
    else:
        windows_size = int(windows_size)
    windowing_type = splitline[4]
    tool = splitline[5]
    tool = tool[:-4]

    return tool, log_name, approach, windowing_type, windows_size
#this funcion extracts information of the archives .txt for the event logs with 9 drift and 5000 traces for VDD
def extracts_information_from_dataset1_VDD_file(file_name):
    file_name_being_analyzed = file_name
    splitline = file_name_being_analyzed.split('_')
    nome_log = splitline[0]
    abordagem = 'trace'
    windows_size = splitline[2]
    windows_size = int(windows_size[4:])
    windowing_type = 'fwin'
    tool = 'vdd'
    win_step=splitline[3]
    win_step=int(win_step[5:])
    return tool, nome_log, abordagem, windowing_type, windows_size, win_step
dic_with_events_dataset1 = {}
dic_with_events_dataset2 = {}

#this fucntion reads the event log as a event stream and find the real drifts
def find_real_drifts_in_xes_file(log_path):
    for root, directories, files in os.walk(log_path):
        for file in files:
            if '1000' in file:
                dic_file = file[:-4]
                dic_file_split = dic_file.split('_')
                dic_file = dic_file_split[0] + '_' + dic_file_split[3] + '_' + \
                           dic_file_split[4]
            else:
                dic_file = file[:-4]
            file_path = os.path.join(log_path, file)
            log = pm4py.read_xes(file_path)
            event_stream = pm4py.convert.convert_to_event_stream(log)
            if '5k' in file:
                real_drifts = calculates_real_drift_when_analyzing_dataset1_as_event_stream(log, event_stream)
                dic_with_events_dataset1[dic_file] = real_drifts
            elif '1000' in file:
                real_drifts = calcula_drift_reais_analise_events_sudden_1000(log, event_stream)
                dic_with_events_dataset2[dic_file] = real_drifts

#this function finds the real drift for the event logs with 5000 traces
def finds_real_drifts_dataset1(approach, file):
    real_drifts_dataset1 = []
    if approach == 'trace':
        real_drifts_dataset1 = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
        return real_drifts_dataset1
    elif approach == 'event':
        splitline_arquivo = file.split('_')
        search_in_dic_file = splitline_arquivo[1]
        for x in dic_with_events_dataset1[search_in_dic_file]:
            real_drifts_dataset1.append(x)
        return real_drifts_dataset1

#this function finds the real drift for the event logs with 1000 traces
def finds_real_drifts_dataset2(approach, arquivo):
    real_drifts_list = []
    if approach == 'trace':
        real_drifts_list = [500]
        return real_drifts_list
    elif approach == 'events':
        file_split = arquivo.split('_')
        file_search = file_split[1] + '_' + file_split[2] + '_' + file_split[3]
        real_drifts = dic_with_events_dataset2[file_search]
        real_drifts_list.append(real_drifts)
        return real_drifts_list


df = pd.DataFrame()

#this function add the data to a pandas dataframe that will be the output of the method
def adiciona_para_dataframe(tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela,
                            f_score):
    linha = [[tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela,
              f_score]]
    df2 = pd.DataFrame(linha, columns=['Tool', 'Nome log', 'Abordagem',
                                       'Tipo janelamento', 'Tamanho da janela',
                                       'F-score'])

    global df
    df = df.append(df2, ignore_index=True)

#this function finds the drifts detected, calculate the F-score and add the F-score and other information to the dataframe
def acha_os_drifts_detectados_calcula_f_score_adiciona_no_df_vdd(f, abordagem, tamanho_da_janela,drifts_reais,
                                                                 tool, nome_log,
                                                                 tipo_janelamento,win_step):
    procura_console_vdd = 'x lines:'
    drift = []
    found = False
    lista_drifts_reais= drifts_reais
    drift_por_cluster = []
    for line in f:
        if found:
            s1 = line.replace('[', '')
            s2 = s1.replace(']', '')
            s3 = s2.replace('\n', '')
            splitline = s3.split(',')

            drift_por_cluster = [int(x) for x in splitline]
            lista_de_drifts_por_traces_vdd = []
            for x in drift_por_cluster:
                trace = x * win_step + 1
                lista_de_drifts_por_traces_vdd.append(trace)
            f_score = F_score_calcule(lista_de_drifts_por_traces_vdd, tamanho_da_janela, 1,
                                      lista_drifts_reais)
            adiciona_para_dataframe(tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela,
                                    f_score)
            break
        if procura_console_vdd in line:
            found = True

# this function finds the detected drifts and calculate de f-score for the toll Apromore ProDrift plugin
def acha_os_drifts_detectados_calcula_f_score_adiciona_no_df_apromore(f, abordagem, tamanho_da_janela, drifts_reais,
                                                                      tool, nome_log, tipo_janelamento):
    drift = []
    for line in f:
        splitline = line.split(' ')
        if len(splitline) > 7:
            if abordagem == 'trace':
                drift.append(int(splitline[6]))
            elif abordagem == 'event':
                drift.append(int(splitline[5]))
    f_score = F_score_calcule(drift, tamanho_da_janela, 9, drifts_reais)
    adiciona_para_dataframe(tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela,
                            f_score)

# this function reads the output from te frameworks and calls the function for F-score calcule
def le_output_dos_frameworks_e_calcula_f_score(caminho_procura):
    for raiz, diretorios, arquivos in os.walk(caminho_procura):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            if '5k' in arquivo:
                if 'apromore' in arquivo:
                    tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela \
                    = extracts_information_from_dataset1_Apromore_file(arquivo)
                elif 'vdd' in arquivo:
                    tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela, win_step \
                        =extracts_information_from_dataset1_VDD_file(arquivo)
                drifts_reais = finds_real_drifts_dataset1(abordagem, arquivo)
            elif '1000' in arquivo:
                if 'apromore' in arquivo:
                    tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela \
                    = extracts_information_from_dataset1_apromore_file(arquivo)
                elif 'vdd' in arquivo:
                    tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela, win_step \
                        = extracts_information_from_dataset2_VDD_file(arquivo)

                drifts_reais = finds_real_drifts_dataset2(abordagem, arquivo)
            with open(caminho_completo, 'r', errors='ignore') as f:
                if 'apromore' in arquivo:
                    acha_os_drifts_detectados_calcula_f_score_adiciona_no_df_apromore(f, abordagem, tamanho_da_janela,
                                                                                      drifts_reais, tool,
                                                                                      nome_log, tipo_janelamento)
                elif 'vdd' in arquivo:
                    acha_os_drifts_detectados_calcula_f_score_adiciona_no_df_vdd(f, abordagem, tamanho_da_janela,
                                                                                 drifts_reais, tool,
                                                                                 nome_log, tipo_janelamento,win_step)


if __name__ == '__main__':
    df = pd.DataFrame()
    
    #here, we put the path to the files
    # the caminho_vdd_sudden_1000 and data/VDD_output_1000 has to be filled with .txt filles that are bigger than 100MB, they have to be downloaded at Kaggle and inputted at the 
    #respective directory 'data/VDD_output_1000' and 'data/VDD_output_5k'. Both files are availabel at https://www.kaggle.com/caioraduy/output-off-vdd-experiments, the must be 
    #downloaded and the directory must be created at the local directory data
    caminho_vdd_sudden_5k
    caminho_procura_5k_apromore = 'data/output_apromore_5k/'
    caminho_procura_5k_apromore_teste = 'data/output_apromore_5k'
    caminho_procura_sudden_1000_apromore = 'data/output_apromore/'
    caminho_procura_sudden_1000_apromore_teste = 'data/output_apromore'
    caminho_vdd_sudden_1000 = 'data/VDD_output_1000'
    caminho_vdd_sudden_5k='data/VDD_output_5k'
    procura_console_vdd = 'x lines:'
  
    caminho_logs_5k = 'data/data_5k/'
    caminho_logs_1000 = 'data/data_1000'
    caminho_logs_5k_teste = 'data/data_5k_teste'
    caminho_logs_1000_teste = 'data/data_teste_sudden'
    
    find_real_drifts_in_xes_file(caminho_logs_5k)
    find_real_drifts_in_xes_file(caminho_logs_1000)
    le_output_dos_frameworks_e_calcula_f_score(caminho_procura_5k_apromore)
    le_output_dos_frameworks_e_calcula_f_score(caminho_procura_sudden_1000_apromore)
    le_output_dos_frameworks_e_calcula_f_score(caminho_vdd_sudden_1000)
    le_output_dos_frameworks_e_calcula_f_score(caminho_vdd_sudden_5k)



    print(df)
    
    df.to_excel('Data\\OutputData\\F_Score_Results.xlsx', index=False)
