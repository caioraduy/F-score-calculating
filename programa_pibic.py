import pm4py
import pandas as pd
import os
def calcula_f_score(list_drifts_detectados, tamanho_janela, numero_de_drifts_reais_da_base, drift_reias):
    dist_max = int(tamanho_janela)
    numero_drifts_reais = numero_de_drifts_reais_da_base
    if numero_de_drifts_reais_da_base == 9:
        drifts_reais = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
    elif numero_de_drifts_reais_da_base == 1:
        drifts_reais = [500]

    list_drifts_detectados = list_drifts_detectados

    drifts_reais.sort()
    tp = []
    fp = []
    mean_delay_diferenca = []
    for x in range(0, len(list_drifts_detectados)):
        for y in range(0, len(drifts_reais)):
            TP_found = False
            distancia = list_drifts_detectados[x] - drifts_reais[y]
            if distancia >= 0 and distancia <= dist_max:
                tp.append(distancia)
                TP_found = True
                drifts_reais.remove(drifts_reais[y])
                break
        if not TP_found:
            fp.append(distancia)
    s = 0
    for x in mean_delay_diferenca:
        s = s + x
    TP = len(tp)
    FP = len(fp)
    FN = numero_drifts_reais - TP
    f_score = TP / (TP + (FP + FN) / 2)

    return f_score
def calcula_drift_reais_analise_events_5k(log,event_stream):
  lista_com_nome_do_trace=[]
  for i in range(500,5000,500):
    x=log[i].attributes['concept:name']
    lista_com_nome_do_trace.append(x)
  lista_drifts_reais_events=[]
  for x in lista_com_nome_do_trace:
    for i, item in enumerate(event_stream):
      if item['case:concept:name']==x:
        lista_drifts_reais_events.append(i)
        break
  return lista_drifts_reais_events
def calcula_drift_reais_analise_events_sudden_1000(log,event_stream):
  drift_real=log[500].attributes['concept:name']
  for i, item in enumerate(event_stream):
      if item['case:concept:name']== drift_real:
        drift_real_event=i
        break
  return  drift_real_event
def extrai_informacao_do_arquivo_base1drift_apromore(nome_do_arquivo):
    nome_do_arquivo_analisado_na_funcao = nome_do_arquivo
    tool='apromore'
    splitline = nome_do_arquivo_analisado_na_funcao.split('_')
    tipo_janelamento = splitline[6]
    abordagem = splitline[4]
    nome_log = splitline[1]+' '+splitline[2]+' '+splitline[3]
    tamanho_da_janela = splitline[5]
    tamanho_da_janela = tamanho_da_janela[2:]
    if tamanho_da_janela== 'default':
        tamanho_da_janela=200
    else:
        tamanho_da_janela=int(tamanho_da_janela)
    return tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela
def extrai_informacao_do_arquivo_base1drift_vdd(nome_do_arquivo):
    nome_do_arquivo_analisado_na_funcao = nome_do_arquivo
    splitline = nome_do_arquivo_analisado_na_funcao.split('_')
    tipo_janelamento = 'fixo'# o vdd só tem janela fixa
    abordagem = splitline[1]
    nome_log = splitline[0]+' '+splitline[3]+' '+splitline[4]
    tamanho_da_janela = splitline[6]
    tamanho_da_janela = int(tamanho_da_janela[4:])
    tool=splitline[9]
    tool=tool[:-4]
    win_step= splitline[7]
    win_step=int(win_step[5:])
    return tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela, win_step
def extrai_informacao_do_arquivo_base9drift_apromore(nome_do_arquivo):
    nome_do_arquivo_analisado_na_funcao = nome_do_arquivo
    splitline = nome_do_arquivo_analisado_na_funcao.split('_')
    nome_log = splitline[1]
    abordagem = splitline[2]
    tamanho_da_janela = splitline[3]
    tamanho_da_janela = tamanho_da_janela[2:]
    if tamanho_da_janela== 'default':
        tamanho_da_janela=200
    else:
        tamanho_da_janela=int(tamanho_da_janela)
    tipo_janelamento = splitline[4]
    tool = splitline[5]
    tool=tool[:-4]
    return tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela

if __name__ == '__main__':
    df = pd.DataFrame()
    caminho_procura_5k_apromore = 'D:/PIBIC/arquivos_analise_programa/trace_9_drift_apromore/'
    caminho_procura_5k_apromore_teste = 'data/output_apromore_5k'
    caminho_procura_sudden_1000_apromore = 'D:/PIBIC/arquivos_analise_programa/trace_1_drift_apromore/'
    caminho_procura_sudden_1000_apromore_teste='data/output_apromore'
    caminho_vdd_sudden_1000 = 'D:/PIBIC/Console_vdd_drift_all/vdd_drift_all_sudden_1000'
    procura_console_vdd = 'x lines:'
    # aqui eu estou lendo os drift reais para as bases de 5k
    caminho_logs = 'data/data_5k_teste/'
    dicionario_com_eventos_5k = {}
    for raiz, diretorios, arquivos in os.walk(caminho_logs):
        for arquivo in arquivos:
            arquivo_para_dic = arquivo[:-4]
            caminho_completo = os.path.join(caminho_logs, arquivo)
            log = pm4py.read_xes(caminho_completo)
            event_stream = pm4py.convert.convert_to_event_stream(log)
            drifts_reais = calcula_drift_reais_analise_events_5k(log, event_stream)
            dicionario_com_eventos_5k[arquivo_para_dic] = drifts_reais
    print(dicionario_com_eventos_5k)

    caminho_logs = 'data/data_teste_sudden/'
    dicionario_com_eventos_1000 = {}
    dicionario_com_eventos_1000 = {}
    for raiz, diretorios, arquivos in os.walk(caminho_logs):
        for arquivo in arquivos:
            arquivo_para_dic = arquivo[:-4]
            arquivo_para_dic_split = arquivo_para_dic.split('_')
            arquivo_para_dic = arquivo_para_dic_split[0] + '_' + arquivo_para_dic_split[3] + '_' + \
                               arquivo_para_dic_split[4]
            print(arquivo_para_dic)
            caminho_completo = os.path.join(caminho_logs, arquivo)
            log = pm4py.read_xes(caminho_completo)
            event_stream = pm4py.convert.convert_to_event_stream(log)
            drifts_reais = calcula_drift_reais_analise_events_sudden_1000(log, event_stream)
            dicionario_com_eventos_1000[arquivo_para_dic] = drifts_reais
    print(dicionario_com_eventos_1000)
    for raiz, diretorios, arquivos in os.walk(caminho_procura_5k_apromore_teste):
    #for raiz, diretorios, arquivos in os.walk(caminho_procura_5k_apromore):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela \
                = extrai_informacao_do_arquivo_base9drift_apromore(arquivo)
            print(abordagem)
            drifts_reais_5k=[]
            if abordagem == 'trace':
                drifts_reais_5k = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
            elif abordagem == 'event':
                splitline_arquivo = arquivo.split('_')
                print(splitline_arquivo)
                arquivo_busca_no_dic = splitline_arquivo[1]
                print(arquivo_busca_no_dic)
                for x in dicionario_com_eventos_5k[arquivo_busca_no_dic]:
                    drifts_reais_5k.append(x)
                print(drifts_reais_5k)
            with open(caminho_completo, 'r', errors='ignore') as f:
                drift = []
                for line in f:
                    splitline = line.split(' ')
                    print(splitline)
                    if len(splitline) >7:
                        if abordagem =='trace':
                            drift.append(int(splitline[6]))
                        elif abordagem == 'event':
                            drift.append(int(splitline[5]))
                print(drift)
                f_score = calcula_f_score(drift, tamanho_da_janela, 9,drifts_reais)
                linha = [[tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela,
                          f_score]]
                df2 = pd.DataFrame(linha, columns=['Tool', 'Nome log', 'Abordagem',
                                                   'Tipo janelamento', 'Tamanho da janela',
                                                   'F-score'])

                df = df.append(df2, ignore_index=True)

    for raiz, diretorios, arquivos in os.walk(caminho_procura_sudden_1000_apromore_teste):
        for arquivo in arquivos:
            splitline = arquivo.split('_')
            caminho_completo = os.path.join(raiz, arquivo)
            tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela \
                = extrai_informacao_do_arquivo_base1drift_apromore(arquivo)
            lista_drifts_reais=[]
            if abordagem == 'trace':
                lista_drifts_reais = [500]
            elif abordagem == 'events':
                arquivo_split = arquivo.split('_')
                arquivo_busca = arquivo_split[1] + '_' + arquivo_split[2] + '_' + arquivo_split[3]
                drifts_reais = dicionario_com_eventos_1000[arquivo_busca]
                lista_drifts_reais.append(drifts_reais)
                print(lista_drifts_reais)
            with open(caminho_completo, 'r', errors='ignore') as f:
                drift = []
                for line in f:
                    splitline = line.split(' ')
                    if len(splitline) == 17:
                        drift.append(int(splitline[6]))
            f_score = calcula_f_score(drift, tamanho_da_janela, 1, lista_drifts_reais)
            linha = [[tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela,
                      f_score]]
            df3 = pd.DataFrame(linha, columns=['Tool', 'Nome log', 'Abordagem',
                                               'Tipo janelamento', 'Tamanho da janela',
                                               'F-score'])

            df = df.append(df3, ignore_index=True)
    for raiz, diretorios, arquivos in os.walk(caminho_vdd_sudden_1000):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela, win_step \
                = extrai_informacao_do_arquivo_base1drift_vdd(arquivo)
            lista_drifts_reais = []
            if abordagem == 'trace':
                lista_drifts_reais = [500]
            elif abordagem == 'events':
                arquivo_split = arquivo.split('_')
                arquivo_busca = arquivo_split[1] + '_' + arquivo_split[2] + '_' + arquivo_split[3]
                drifts_reais = dicionario_com_eventos_1000[arquivo_busca]
                lista_drifts_reais.append(drifts_reais)
                print(lista_drifts_reais)
            with open(caminho_completo, 'r', errors='ignore') as f:
                drift = []
                found = False
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
                        f_score = calcula_f_score(lista_de_drifts_por_traces_vdd, tamanho_da_janela,1,lista_drifts_reais)
                        linha = [[tool, nome_log, abordagem, tipo_janelamento, tamanho_da_janela,
                                  f_score]]
                        df4 = pd.DataFrame(linha, columns=['Tool', 'Nome log', 'Abordagem',
                                                           'Tipo janelamento', 'Tamanho da janela',
                                                           'F-score'])

                        df = df.append(df4, ignore_index=True)
                        break
                    if procura_console_vdd in line:
                        found = True
    print(df)
    df.to_excel('D:\\PIBIC\\resultados_pibic\\resultados_logs_ddm_runs.xlsx', index=False)