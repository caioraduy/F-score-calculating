import pandas as pd
from scipy.stats import wilcoxon
def aplica_wilcoxon(Tool):
    print(f'-------------{Tool}----------------')
# Task 1: Read the data from the first sheet
    df = pd.read_excel('C:\\Users\\raduy\\PycharmProjects\\F-score-calculating\\data\\outputdata\\F_Score_Results.xlsx')

# Task 2: Filter and group by 'Event Log Name' and calculate F-score
    filtered_df = df[ (df['Tool'] == Tool)]

    filtered_df = filtered_df[ filtered_df['Approach'] == 'adaptive']

    filtered_df = filtered_df[filtered_df["Window's size"] != 25]

    filtered_df.loc[filtered_df['Event Log Name'] == 'lp2.5k', 'Event Log Name'] = 'lp5k'
    filtered_df.loc[filtered_df['Event Log Name'] == 're2.5k', 'Event Log Name'] = 're5k'
    grouped_df = filtered_df.groupby('Event Log Name')['F-score'].apply(list).reset_index()

# Task 3: Save the grouped data to a new Excel sheet
    grouped_df.to_excel(f'C:\\Users\\raduy\\PycharmProjects\\F-score-calculating\\data\\outputdata\\Grouped_F_Score_{Tool}.xlsx', index=False)

# Task 4: Create the list of patterns
    ch = ['cb5k', 'cd5k', 'cf5k', 'cm5k', 'cp5k', 'IOR5k', 'IRO5k', 'lp5k', 'OIR5k', 'ORI5k', 'pl5k', 'pm5k', 're5k', 'RIO5k', 'ROI5k', 'rp5k', 'sw5k']

# Task 5: Perform the Wilcoxon test
    results = []
    for pattern in ch:
        for i in range(0, 10):

            sample1 = filtered_df[filtered_df['Event Log Name'] == f'{pattern}']['F-score']
            sample2 = filtered_df[filtered_df['Event Log Name'] == f'{pattern}_LOGGEN_{i}']['F-score']

            zero_sample_1 = sum(sample1.isin([0]))
            zero_sample_2 = sum(sample2.isin([0]))
            one_sample_1 = sum(sample1.isin([1]))
            one_sample_2 = sum(sample2.isin([1]))

            if len(sample1) != 8:
                print("Erro, nos tamanho das amostras",pattern)

            elif sample1.equals(sample2):
                print('Erro, as amostras são identicas')

            elif zero_sample_1 == 8 or zero_sample_2 == 8:

                results.append((pattern, f'{pattern}', f'{pattern}_LOGGEN_{i}', "Amostras com zero"))

            elif one_sample_1 ==8 and one_sample_2 ==8:
                results.append((pattern, f'{pattern}', f'{pattern}_LOGGEN_{i}', "Elementos iguais a 1"))
            else:
                #print(f'-------{pattern}  {i}-----------')
                #print(sample1)
                #print(sample2)
                w, p_value = wilcoxon(sample1, sample2, zero_method='wilcox', alternative = "two-sided",method = "approx")
                results.append((pattern, f'{pattern}', f'{pattern}_LOGGEN_{i}', p_value, w))



    # Print the results
    for result in results:
        if not isinstance(result[3], str):
            if result[3] < 0.05:
                print(f'({result[1]} x {result[2]})-> W:{result[4]} p-value: {result[3]}---Existe diferença')
            elif result[3] > 0.05:
                print(f'({result[1]} x {result[2]})-> W:{result[4]} p-value: {result[3]}--- NÃO Existe diferença')
        else:
            print(f'({result[1]} x {result[2]})->{result[3]}')



if __name__ =='__main__':
    aplica_wilcoxon('IPDD')
    aplica_wilcoxon("Apromore - ProDrift")
