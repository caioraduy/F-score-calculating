    # drifts_detectados = int(input('Entre com o numero de drifts detectados:'))
def ProM_F_score_calculation(drifts_detected=[], real_drifts=[]):
    # # dist_max = int(input(Entre a distancia mÃ¡xima permitida para ser considerado o drift:"))
    dist_max = 100
    # distancia_entre_drifts = traces = int(input('Input the number of
    # traces between the real drifts:'))


    #Here,we have to input the Output of

    # here, we have to enter the number of real drift in the synthetic log
    numero_drifts_reais = len(real_drifts)
    # here we have to input which is/are the trace(s) that has(ve) real drifts
    # if the tested event log is from data_1000, we input numero_drifts_reais = 1 and
    # drifts_reais = [500]. However, if we are testing a event log from data_5k, we input
    # numero_drifts_reais = 9 and drifts_reais = [500, 1000, 1500, 2000, 2500,
    # 3000,3500,4000,4500]
    drifts_reais = real_drifts
    if len(drifts_reais)==0:
        return print('you must input the real drifts, please try again')
    drifts_reais.sort()

    #Here, we register de drifts detected that has to manually inputted
    #because of the fact that the output of the ProM
    list_drifts_detectados = drifts_detected
    list_drifts_detectados.sort()
    tp = []
    fp = []

    lista_drifts_reais_detectados = []
    for x in range(0, len(list_drifts_detectados)):
        TP_found = False
        for y in range(0, len(drifts_reais)):
            distancia = list_drifts_detectados[x] - drifts_reais[y]
            if distancia >= 0 and distancia <= dist_max:
                tp.append(distancia)
                TP_found = True
                drifts_reais.remove(drifts_reais[y])
                break
        if not TP_found:
            fp.append(distancia)


    TP = len(tp)
    FP = len(fp)
    FN = numero_drifts_reais - TP

    F = TP / (TP + (FP + FN) / 2)

    print(f'TP: {TP}')
    print(f'FP: {FP}')
    print(f'FN: {FN}')
    print(f'The F-score is: {F}')
# the first parameter we have to input is a list whit the drifts detected by the framework
#and the second is the real drift localization
f=ProM_F_score_calculation([1],[400])
print(f)