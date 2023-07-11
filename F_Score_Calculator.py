import pm4py
import pandas as pd
import os


# Function that calculates the F-score using a list of real drifts and a list of reported drifts
# A real drift is considered correctly detected when there is a reported drift in the interval
# [real drift, real drift + error tolerance]
# tp -> true positives: incremented for all correctly detected drifts
# fp -> false positives: incremented for all reported drifts not correctly detected
# fn -> false negatives: incremented for all real drifts not detected in the reported drifts
def calculate_f_score(detected_drifts_list, real_drifts, error_tolerance):
    real_drifts_cp = real_drifts.copy()
    number_of_real_drifts = len(real_drifts_cp)
    real_drifts_cp.sort()
    tp_list = []
    fp_list = []
    # here we compare the drifts detected and add the TP or FP
    for x in range(0, len(detected_drifts_list)):
        tp_found = False
        for y in range(0, len(real_drifts_cp)):
            dist = detected_drifts_list[x] - real_drifts_cp[y]
            # we only consider the drift detected as TP, if the drift is detected after
            # the real drift and the error tolerance is lower than the window size
            if 0 <= dist <= error_tolerance:
                tp_list.append(dist)
                tp_found = True
                real_drifts_cp.remove(real_drifts_cp[y])
                break
        if not tp_found:
            fp_list.append(detected_drifts_list[x])
    tp = len(tp_list)
    fp = len(fp_list)
    if (tp + fp) != len(detected_drifts_list):
        # just to confirm that each detect drift is counted as a TP or FP
        # this message must not be shown
        print(f'F-score with problems!')
    fn = number_of_real_drifts - tp
    f_score = tp / (tp + (fp + fn) / 2)

    return f_score


# This function calculates real drifts of the base with 5000 trace and 9 drifts
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


# This function calculates real drifts of the base with 1000 trace and 1 drifts, when reading
# the file as an event stream
# not used because we applied the approach based on traces (runs approach)
def calcula_drift_reais_analise_events_sudden_1000(log, event_stream):
    real_drift = log[500].attributes['concept:name']
    for i, item in enumerate(event_stream):
        if item['case:concept:name'] == real_drift:
            real_drift_index_when_reading_as_event_stream = i
            break
    return real_drift_index_when_reading_as_event_stream


# this function extracts the information of the file with the output of ProDrift Plugin
def extracts_information_from_dataset2_apromore_file(file_name):
    start = file_name.find("log_") + len("log_")
    end = file_name.find("_trace_ws")
    log_name = file_name[start:end]

    splitline = file_name[end + 1:].split('_')
    tool = 'Apromore - ProDrift'
    approach = splitline[0]
    windows_size = splitline[1]
    windows_size = windows_size[2:]
    windowing_type = splitline[2]
    if windowing_type == 'fwin':  # for using the name in the paper
        windowing_type = 'fixed'
    # log_name = splitline[1] + ' ' + splitline[2] + ' ' + splitline[3]

    if windows_size == 'default':
        windows_size = 200
    else:
        windows_size = int(windows_size)

    return tool, log_name, approach, windowing_type, windows_size


# this function extracts information from the archive of the bases with 1000 and 1 drift a VDD
def extracts_information_from_dataset2_VDD_file(file_name):
    print(f'Get information from VDD: {file_name}')
    file_name_being_analyzed = file_name
    splitline = file_name_being_analyzed.split('_')
    windowing_type = 'fixed'
    approach = splitline[1]
    log_name = splitline[0] + ' ' + splitline[3] + ' ' + splitline[4]
    windows_size = splitline[6]
    windows_size = int(windows_size[4:])
    tool = 'VDD'
    win_step = splitline[7]
    win_step = int(win_step[5:])


    return tool, log_name, approach, windowing_type, windows_size, win_step

def extracts_information_from_dataset1_IPDD_file(file_name):
    #print(f'Get information from IPDD framework: {file_name}')
    file_name_being_analyzed = file_name
    splitline = file_name_being_analyzed.split('_')
    if 'LOGGENERATOR' in file_name:
        log_name = splitline[1]+' '+splitline[2]
        approach = 'Trace'
        windows_size = splitline[3]
        if windows_size == None:
            print("erro")
        windows_size = windows_size[2:]
        windows_size = int(windows_size)
        windowing_type = splitline[4]
        windowing_type = windowing_type[0:-4]
    else:
        log_name = splitline[1]
        approach = 'Trace'
        windows_size = splitline[2]
        if windows_size == None:
            print("erro")
            print(windows_size)
        print(file_name)
        windows_size = windows_size[2:]
        windows_size = int(windows_size)
        windowing_type = splitline[3]
        windowing_type = windowing_type[0:-4]


    #print(windowing_type)
    if windowing_type == None:
        print(file_name)

    tool = 'IPDD'
    dataset = 1
    real_drift = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
    #print(log_name)
    return tool, log_name, approach, windowing_type, windows_size, dataset, real_drift

def extracts_information_from_dataset2_IPDD_file(file_name):
    #print(f'Get information from IPDD framework: {file_name}')
    file_name_being_analyzed = file_name
    splitline = file_name_being_analyzed.split('_')
    log_name = splitline[1] +'_' + splitline[2] + '_' + splitline[3] +'_'+ splitline[4] +'_'+ splitline[5]
    approach = 'Trace'
    windows_size = splitline[-2]
    if windows_size == None:
        print("erro")
    #print(windows_size)
    windows_size = windows_size[2:]
    windows_size = int(windows_size)

    windowing_type = splitline[7]
    windowing_type = windowing_type[0:-4]
    #print(windowing_type)
    if windowing_type == None:
        print(file_name)

    tool = 'IPDD'
    dataset = 2
    real_drift =[500]
    #print(log_name)
    return tool, log_name, approach, windowing_type, windows_size, dataset, real_drift


# this function extracts information of the archives .txt for the event logs
# with 9 drift and 5000 traces for Apromore
def extracts_information_from_dataset1_apromore_file(file_name):
    if 'LOGGEN' in file_name:
        file_name_being_analyzed = file_name
        splitline = file_name_being_analyzed.split('_')
        log_name = splitline[0]+ '_' +splitline[1] + '_'+ splitline[2]
        approach = splitline[3]
        windows_size = splitline[4]
        windows_size = windows_size[2:]
        if windows_size == 'default':
            windows_size = 200
        else:
            windows_size = int(windows_size)
        windowing_type = splitline[5]
        if windowing_type == 'fwin':  # for using the name in the paper
            windowing_type = 'fixed'
        tool = 'Apromore - ProDrift'
    else:
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
        if windowing_type == 'fwin':  # for using the name in the paper
            windowing_type = 'fixed'
        tool = 'Apromore - ProDrift'


    return tool, log_name, approach, windowing_type, windows_size


# extracts information from name of the outputted VDD's files - IPDD_dataset1
def extracts_information_from_dataset1_VDD_file(file_name):
    print(f'Get information from VDD: {file_name}')
    file_name_being_analyzed = file_name
    splitline = file_name_being_analyzed.split('_')
    nome_log = splitline[0]
    approach = 'trace'
    windows_size = splitline[2]
    windows_size = int(windows_size[4:])
    windowing_type = 'fixed'
    tool = 'VDD'
    win_step = splitline[3]
    win_step = int(win_step[5:])
    return tool, nome_log, approach, windowing_type, windows_size, win_step


dic_with_events_dataset1 = {}
dic_with_events_dataset2 = {}


# reads the event log as a event stream and find the real drifts
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


# this function finds the real drift for the event logs with 5000 traces
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


# this function finds the real drift for the event logs with 1000 traces
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

# finds the detected drifts, VDD only reports the windows with drift, so we have to identify the trace index
# then the function calculates the F-score and returns it into a list
def find_detected_drift_and_calculate_f_score_vdd(f, approach,
                                                  window_size,
                                                  real_drifts, tool, log_name, windowing_type,
                                                  win_step):
    search_in_vdd_console = 'x lines:'
    drift = []
    found = False
    real_drift_list = real_drifts
    window_with_drift = []
    new_line = None
    for line in f:
        if found:
            s1 = line.replace('[', '')
            s2 = s1.replace(']', '')
            s3 = s2.replace('\n', '')
            splitline = s3.split(',')

            window_with_drift = [int(x) for x in splitline]
            trace_with_drift_VDD = []
            for x in window_with_drift:
                trace = x * win_step + 1
                trace_with_drift_VDD.append(trace)
            f_score = calculate_f_score(trace_with_drift_VDD, real_drift_list, window_size)
            if len(real_drifts) == 9:
                dataset = 1
            else:
                dataset = 2
            new_line = {'Tool': tool,
                        'Dataset': dataset,
                        'Event Log Name': log_name,
                        'Approach': windowing_type,
                        "Window's size": window_size,
                        'F-score': f_score,
                        'Real drifts': real_drift_list,
                        'Detected drifts': trace_with_drift_VDD}
            break
        if search_in_vdd_console in line:
            found = True
    return new_line

def find_detected_drift_and_f_score_IPDD(f, tool, log_name, approach, windowing_type, windows_size,
                                                dataset, real_drift):

    search_in_IPDD_console_detected_drifts = 'IPDD detect control-flow drift in windows'
    search_in_IPDD_console_detected_drifts_adaptive = 'Similarity metrics confirm the drifts in'
    search_in_IPDD_console_zero_detected_drift_adaptive = 'Adaptive IPDD detect control-flow drifts in traces []'
    drift = []
    found_adaptive = False
    found_fixed = False

    for line in f:
        if search_in_IPDD_console_zero_detected_drift_adaptive in line:
            detected_drift = []
        elif search_in_IPDD_console_detected_drifts_adaptive in line:
            found_adaptive = True
            detected_drift = line.split('[')
            detected_drift = detected_drift[1].split(']')
            detected_drift = detected_drift[0]
            detected_drift = detected_drift.split(',')


            for i in range(0, len(detected_drift)):
                if not detected_drift[i]:
                    detected_drift[i] = 0
                detected_drift[i] = int(detected_drift[i])


        elif search_in_IPDD_console_detected_drifts in line:
            found_fixed = True
            print(line)
            splitline = line.split('traces')
            print(splitline)
            # LISTA DE DRIFTS REAIS
            detected_drift = splitline[1].split('[')
            print(detected_drift)
            detected_drift = detected_drift[1].split(']')
            print('----------')
            print(detected_drift)
            detected_drift = detected_drift[0].split(',')
            print(detected_drift)

            for i in range(0, len(detected_drift)):
                if not detected_drift[i]:
                    detected_drift[i] = 0
                detected_drift[i] = int(detected_drift[i])
            #print(real_drift)
            #LISTA DE DRIFTS DETECTADOS

        elif found_adaptive:
            pass
        elif found_fixed:
            pass
    print(detected_drift)

    f_score = calculate_f_score(detected_drift, real_drift, 100)



    new_line = {'Tool': tool,
                        'Dataset': dataset,
                        'Event Log Name': log_name,
                        'Approach': windowing_type,
                        "Window's size": windows_size,
                        'F-score': f_score,
                        'Real drifts': real_drift,
                        'Detected drifts': detected_drift}
    print(new_line)





    return new_line

# finds the detected drifts and calculates de f-score for the tool Apromore ProDrift plugin
def find_detected_drifts_calcule_f_score_apromore(f, approach, window_size, real_drifts,
                                                  tool, log_name, windowing_type):
    drift = []
    for line in f:
        splitline = line.split(' ')
        if len(splitline) > 7:
            if approach == 'trace':
                drift.append(int(splitline[6]))
            elif approach == 'event':
                drift.append(int(splitline[5]))
    f_score = 0
    if windowing_type == 'adaptive':
        # using 100 as error tolerance when evaluating adaptive approaches
        f_score = calculate_f_score(drift, real_drifts, window_size)
    else:
        f_score = calculate_f_score(drift, real_drifts, window_size)
    if len(real_drifts) == 9:
        dataset = 1
    else:
        dataset = 2
    new_line = {'Tool': tool,
                'Dataset': dataset,
                'Event Log Name': log_name,
                'Approach': windowing_type,
                "Window's size": window_size,
                'F-score': f_score,
                'Real drifts': real_drifts,
                'Detected drifts': drift}
    return new_line


# The ProM framework reports the change points in the plot
# Because of this we inputted the detected drifts manually in the main function
def calculate_prom_f_score(log_name, detected_drifts, real_drifts, error_tolerance):
    f_score = calculate_f_score(detected_drifts, real_drifts, error_tolerance)
    if len(real_drifts) == 9:
        dataset = 1
    else:
        dataset = 2
    new_line = {'Tool': 'ProM - Concept Drift',
                'Dataset': dataset,
                'Event Log Name': log_name,
                'Approach': 'adaptive',
                "Window's size": '',
                'F-score': f_score,
                'Real drifts': real_drifts,
                'Detected drifts': detected_drifts}
    return new_line


# this function reads the output from te frameworks and calls the function for F-score calcule
def read_framework_output_and_calculate_f_score(path_search):
    f_scores_complete = []
    approach = 'trace'
    for root, directories, files in os.walk(path_search):
        for file in files:
            full_path = os.path.join(root, file)
            if '5k' in file:
                if 'apromore' in file:
                    tool, log_name, approach, windowing_type, window_size \
                        = extracts_information_from_dataset1_apromore_file(file)
                elif 'vdd' in file:
                    tool, log_name, approach, windowing_type, window_size, win_step \
                        = extracts_information_from_dataset1_VDD_file(file)
                elif 'IPDD' in file:
                    tool, log_name, approach, windowing_type, window_size, dataset,\
                    real_drift = extracts_information_from_dataset1_IPDD_file(file)

                real_drifts = finds_real_drifts_dataset1(approach, file)
            elif '1000' in file:
                if 'apromore' in file:
                    tool, log_name, approach, windowing_type, window_size \
                        = extracts_information_from_dataset2_apromore_file(file)
                elif 'vdd' in file:
                    tool, log_name, approach, windowing_type, window_size, win_step \
                        = extracts_information_from_dataset2_VDD_file(file)
                elif 'IPDD' in file:
                    tool, log_name, approach, windowing_type, window_size, dataset,\
                        real_drift = extracts_information_from_dataset2_IPDD_file(file)

                real_drifts = finds_real_drifts_dataset2(approach, file)
            with open(full_path, 'r', errors='ignore') as f:

                if 'apromore' in file:
                    f_scores_complete.append(find_detected_drifts_calcule_f_score_apromore(f, approach, window_size,
                                                                                           real_drifts, tool,
                                                                                           log_name, windowing_type))
                elif 'vdd' in file:
                    f_scores_complete.append(find_detected_drift_and_calculate_f_score_vdd(f, approach, window_size,
                                                                                           real_drifts, tool,
                                                                                           log_name, windowing_type,
                                                                                           win_step))
                elif 'IPDD' in file:
                    f_scores_complete.append(find_detected_drift_and_f_score_IPDD(f, tool, log_name, approach,
                                                                                  windowing_type, window_size,
                                                                                  dataset, real_drift))
    return f_scores_complete


def get_prom_f_scores_dataset1(real_drifts_dataset1, et):
    print(f'Calculating f-score for ProM Concept Drift - dataset1')
    f_scores_ds1 = []
    detected_drifts = [360]
    f_scores_ds1.append(calculate_prom_f_score('cb5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = []
    f_scores_ds1.append(calculate_prom_f_score('cd5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = [510, 995, 1508, 1998, 2498, 2996, 3498, 3998, 4486]
    f_scores_ds1.append(calculate_prom_f_score('cf5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = [493]
    f_scores_ds1.append(calculate_prom_f_score('cm5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = [519, 1000, 1506, 1996, 2493, 2931, 3501, 3997, 4504]
    f_scores_ds1.append(calculate_prom_f_score('cp5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = []
    f_scores_ds1.append(calculate_prom_f_score('fr5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = []
    f_scores_ds1.append(calculate_prom_f_score('IOR5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = [3499]
    f_scores_ds1.append(calculate_prom_f_score('IRO5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = [502]
    f_scores_ds1.append(calculate_prom_f_score('lp2.5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = [506, 999, 1509, 1997, 2502, 2999, 3487, 3999, 4498]
    f_scores_ds1.append(calculate_prom_f_score('OIR5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = [508, 995, 1521, 1951, 2495, 2990, 3509, 3978, 4501]
    f_scores_ds1.append(calculate_prom_f_score('ORI5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = []
    f_scores_ds1.append(calculate_prom_f_score('pl5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = [360]
    f_scores_ds1.append(calculate_prom_f_score('pm5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = [502, 1006, 1505, 1998, 2501, 3000, 3499, 3999, 4499]
    f_scores_ds1.append(calculate_prom_f_score('re2.5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = []
    f_scores_ds1.append(calculate_prom_f_score('RIO5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = []
    f_scores_ds1.append(calculate_prom_f_score('ROI5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = []
    f_scores_ds1.append(calculate_prom_f_score('rp5k', detected_drifts, real_drifts_dataset1, et))
    detected_drifts = []
    f_scores_ds1.append(calculate_prom_f_score('sw5k', detected_drifts, real_drifts_dataset1, et))
    return f_scores_ds1


def get_prom_f_scores_dataset2(real_drifts_dataset2, et):
    print(f'Calculating f-score for ProM Concept Drift - dataset2')
    f_scores_ds2 = []
    detected_drifts = [464]
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_cb', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = [532]
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_cd', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = [398]
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_cf', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = [449]
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_cp', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = []
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_IOR', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = [352]
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_IRO', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = [535]
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_lp', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = [468]
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_OIR', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = []
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_pl', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = [509]
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_pm', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = [484]
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_re', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = [555]
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_RIO', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = [532]
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_ROI', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = []
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_rp', detected_drifts,
                                                         real_drifts_dataset2, et))
    detected_drifts = []
    f_scores_ds2.append(calculate_prom_f_score('sudden_trace_noise0_1000_sw', detected_drifts,
                                                         real_drifts_dataset2, et))
    return f_scores_ds2


if __name__ == '__main__':
    # Path to the files containing the output of the selected tools
    # The path_vdd_sudden_dataset1 and path_vdd_sudden_dataset2 points to the folders where the .txt files outputted
    # by VDD should be placed
    # The files must be downloaded from Kaggle and copied into the folder because the files contains more than 100MB
    # Both files are available at https://www.kaggle.com/caioraduy/output-off-vdd-experiments
    path_output_apromore_dataset1 = os.path.join('data', 'output_apromore_dataset1')
    path_output_apromore_dataset2 = os.path.join('data', 'output_apromore_dataset2')
    path_vdd_sudden_dataset1 = os.path.join('data', 'output_vdd_dataset1')
    path_vdd_sudden_dataset2 = os.path.join('data', 'output_vdd_dataset2')
    path_IPDD_sudden_dataset1 = os.path.join('data', 'output_IPDD_dataset1_old')
    path_IPDD_sudden_dataset2 = os.path.join('data', 'output_IPDD_dataset2')
    teste_LOGGEN = os.path.join('data', 'base_5k_copia')
    teste_LOGGEN2 = os.path.join('data', 'base5k_copia_APROMORE')
    AnaliseSensibilidade_apromore = os.path.join('data', 'AnaliseSensibilidadeApromore')


    vdd_match_string_change_points = 'x lines:'

    # path to the original event logs
    path_logs_5k = os.path.join('data', 'data_5k')
    path_logs_1000 = os.path.join('data', 'data_1000')

    # list containing all the calculated f_scores
    f_scores = []
    #APROMORE
    f_scores = f_scores + read_framework_output_and_calculate_f_score(path_output_apromore_dataset1)
    #f_scores = f_scores + read_framework_output_and_calculate_f_score(path_output_apromore_dataset2)

    #IPDD
    #f_scores = f_scores + read_framework_output_and_calculate_f_score(path_IPDD_sudden_dataset1)
    #f_scores = f_scores + read_framework_output_and_calculate_f_score(path_IPDD_sudden_dataset2)


    # VDD
   #f_scores = f_scores + read_framework_output_and_calculate_f_score(path_vdd_sudden_dataset1)
    #f_scores = f_scores + read_framework_output_and_calculate_f_score(path_vdd_sudden_dataset2)

    #f_scores = f_scores + read_framework_output_and_calculate_f_score(path_IPDD_sudden_fixed)
    #f_scores = f_scores + read_framework_output_and_calculate_f_score(teste_LOGGEN)
    #f_scores = f_scores + read_framework_output_and_calculate_f_score(teste_LOGGEN2)

    #analise de sensibilidade do apromore usando o loggen
    f_scores = f_scores + read_framework_output_and_calculate_f_score(AnaliseSensibilidade_apromore)





    # for the ProM Concept Drift we have to manually input the detected drifts based on the
    # information from the plots
    # Dataset 1
    #real_drifts_dataset1 = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
    #et = 100
    #f_scores = f_scores + get_prom_f_scores_dataset1(real_drifts_dataset1, et)
    # Dataset 2
    #real_drifts_dataset2 = [500]
    #et = 100
    #f_scores = f_scores + get_prom_f_scores_dataset2(real_drifts_dataset2, et)


    #print(f_scores)
    #for i in f_scores:
        #print(i)
        #for j in i:
            #if j == None:
                #print(i)
                #print(j)
    #print(f_scores)
    #for i in f_scores:

        #print(i)
    # convert to dataframe
    df = pd.DataFrame(f_scores)
    output_path = os.path.join('data', 'outputdata')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_filename = os.path.join(output_path, 'F_Score_Results.xlsx')
    # export to excel file
    df.to_excel(output_filename, index=False)