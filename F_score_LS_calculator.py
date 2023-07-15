import pm4py
import pandas as pd
import os

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

dic_with_events_dataset1 = {}
dic_with_events_dataset2 = {}






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




# this function reads the output from te frameworks and calls the function for F-score calcule
def read_framework_output_and_calculate_f_score(path_search):
    f_scores_complete = []
    approach = 'trace'
    for root, directories, files in os.walk(path_search):
        for file in files:
            full_path = os.path.join(root, file)

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
            elif 'LS' in file:
                if 'apromore' in file:
                    tool, log_name, approach, windowing_type, window_size \
                        = extracts_information_from_dataset4_apromore_file(file)
                elif 'vdd' in file:
                    tool, log_name, approach, windowing_type, window_size, win_step \
                        = extracts_information_from_dataset4_VDD_file(file)
                elif 'IPDD' in file:
                    tool, log_name, approach, windowing_type, window_size, dataset,\
                        real_drift = extracts_information_from_dataset4_IPDD_file(file)

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


if __name__ == '__main__':

    dataset4_apromore = os.path.join('data', 'Apromore_dataset4')
    dataset4_IPDD = os.path.join('data', 'IPDD_dataset4')
    dataset4_vdd = os.path.join('data', 'VDD_dataset4')



    vdd_match_string_change_points = 'x lines:'


    # DATASET4
    f_scores = f_scores + read_framework_output_and_calculate_f_score(dataset4_apromore)
    f_scores = f_scores + read_framework_output_and_calculate_f_score(dataset4_IPDD)
    f_scores = f_scores + read_framework_output_and_calculate_f_score(dataset4_vdd)






    df = pd.DataFrame(f_scores)
    output_path = os.path.join('data', 'outputdata')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_filename = os.path.join(output_path, 'F_Score_Results_DATASET4.xlsx')
    # export to excel file
    df.to_excel(output_filename, index=False)