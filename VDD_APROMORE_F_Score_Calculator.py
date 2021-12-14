import pm4py
import pandas as pd
import os


# This is one of the most important function of the program,
# it uses the TP, FP, FN for
# calculating the F-score
def calculate_f_score(detected_drifts_list, win_size, real_drifts):
    real_drifts_cp = real_drifts.copy()
    error_tolerance = int(win_size)
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

    splitline = file_name[end+1:].split('_')
    tool = 'Apromore - ProDrift'
    approach = splitline[0]
    windows_size = splitline[1]
    windows_size = windows_size[2:]
    windowing_type = splitline[2]
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


# this funcion extracts information of the archives .txt for the event logs
# with 9 drift and 5000 traces for Apromore
def extracts_information_from_dataset1_apromore_file(file_name):
    print(f'Get information from Apromore: {file_name}')
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
    tool = 'Apromore - ProDrift'

    return tool, log_name, approach, windowing_type, windows_size


# extracts information from name of the outputted VDD's files - dataset1
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


# df = pd.DataFrame()
#
#
# # this function add the data to a pandas dataframe that will be the output of the method
# def add_to_dataframe(tool, log_name, approach, windowing_type, window_size,
#                      f_score):
#     line = [[tool, log_name, approach, windowing_type, window_size,
#              f_score]]
#     df2 = pd.DataFrame(line, columns=['Tool', 'Log name', 'Approach',
#                                       'Windowing type', 'Window size',
#                                       'F-score'])
#
#     global df
#     df = df.append(df2, ignore_index=True)


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
            f_score = calculate_f_score(trace_with_drift_VDD, window_size, real_drift_list)
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
            # add_to_dataframe(tool, log_name, approach, windowing_type, window_size,
            #                  f_score)
            break
        if search_in_vdd_console in line:
            found = True
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
    f_score = calculate_f_score(drift, window_size, real_drifts)
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
    # add_to_dataframe(tool, log_name, approach, windowing_type, window_size,
    #                  f_score)


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
                real_drifts = finds_real_drifts_dataset1(approach, file)
            elif '1000' in file:
                if 'apromore' in file:
                    tool, log_name, approach, windowing_type, window_size \
                        = extracts_information_from_dataset2_apromore_file(file)
                elif 'vdd' in file:
                    tool, log_name, approach, windowing_type, window_size, win_step \
                        = extracts_information_from_dataset2_VDD_file(file)

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
    return f_scores_complete


if __name__ == '__main__':
    # df = pd.DataFrame()

    # Path to the files containing the output of the selected tools
    # The path_vdd_sudden_dataset1 and path_vdd_sudden_dataset2 points to the folders where the .txt files outputted
    # by VDD should be placed
    # The files must be downloaded from Kaggle and copied into the folder because the files contains more than 100MB
    # Both files are available at https://www.kaggle.com/caioraduy/output-off-vdd-experiments
    path_output_apromore_dataset1 = os.path.join('data', 'output_apromore_dataset1')
    path_output_apromore_dataset2 = os.path.join('data', 'output_apromore_dataset2')
    path_vdd_sudden_dataset1 = os.path.join('data', 'output_vdd_dataset1')
    path_vdd_sudden_dataset2 = os.path.join('data', 'output_vdd_dataset2')
    vdd_match_string_change_points = 'x lines:'

    # path to the original event logs
    path_logs_5k = os.path.join('data', 'data_5k')
    path_logs_1000 = os.path.join('data', 'data_1000')

    # find_real_drifts_in_xes_file(path_logs_5k)
    # find_real_drifts_in_xes_file(path_logs_1000)
    f_scores = []
    f_scores = f_scores + read_framework_output_and_calculate_f_score(path_output_apromore_dataset1)
    f_scores = f_scores + read_framework_output_and_calculate_f_score(path_output_apromore_dataset2)
    f_scores = f_scores + read_framework_output_and_calculate_f_score(path_vdd_sudden_dataset1)
    f_scores = f_scores + read_framework_output_and_calculate_f_score(path_vdd_sudden_dataset2)
    df = pd.DataFrame(f_scores)

    # print(df)
    output_path = os.path.join('data', 'outputdata')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_filename = os.path.join(output_path, 'F_Score_Results.xlsx')
    df.to_excel(output_filename, index=False)
