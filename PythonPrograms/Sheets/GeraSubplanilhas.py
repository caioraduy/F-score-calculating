import pandas as pd

# Carregar os dados do Excel em um DataFrame do pandas
df = pd.read_excel('C:\\Users\\raduy\\PycharmProjects\\F-score-calculating\\data\\outputdata\\F_Score_Results.xlsx')

# Filtrar as colunas relevantes
relevant_columns = ['Event Log Name', "Window's size", 'F-score']
df_filtered = df[relevant_columns]

# Criar um dicionário para armazenar as tabelas separadas
tables = {}

# Obter os diferentes valores de 'Window's size' e ordená-los
window_sizes = sorted(df_filtered["Window's size"].unique())

# Iterar sobre cada linha do DataFrame
for index, row in df_filtered.iterrows():
    event_log = row['Event Log Name']
    window_size = row["Window's size"]
    fscore = row['F-score']

    # Extrair o índice presente no 'Event Log Name'
    event_log_num = ''.join(filter(str.isdigit, event_log))

    # Criar ou adicionar o valor na tabela correspondente ao evento de log
    if event_log_num not in tables:
        tables[event_log_num] = pd.DataFrame(columns=['Event Log Name'] + window_sizes)

    table = tables[event_log_num]

    if event_log in table['Event Log Name'].values:
        # Atualizar o valor do fscore na tabela existente
        table.loc[table['Event Log Name'] == event_log, window_size] = fscore
    else:
        # Criar uma nova linha com o fscore
        new_row = [''] * (len(window_sizes) + 1)
        new_row[0] = event_log
        new_row[window_sizes.index(window_size) + 1] = fscore
        table.loc[len(table)] = new_row

# Salvar as tabelas em arquivos separados com o nome correto
for event_log_num, table in tables.items():
    filename = f"Resultados_f_score_apromore_geracao{event_log_num}.xlsx"
    table.to_excel(filename, index=False)
    print(f"Tabela para o evento de log '{event_log_num}' foi salva em '{filename}'.")