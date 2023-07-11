import pandas as pd
from scipy.stats import wilcoxon

# Task 1: Read the data from the first sheet
df = pd.read_excel('C:\\Users\\raduy\\PycharmProjects\\F-score-calculating\\data\\outputdata\\F_Score_Results.xlsx')

# Task 2: Filter and group by 'Event Log Name' and calculate F-score
filtered_df = df[ (df['Approach'] == 'adaptive')]
filtered_df.loc[filtered_df['Event Log Name'] == 'lp2.5k', 'Event Log Name'] = 'lp5k'
filtered_df.loc[filtered_df['Event Log Name'] == 're2.5k', 'Event Log Name'] = 're5k'
grouped_df = filtered_df.groupby('Event Log Name')['F-score'].apply(list).reset_index()

# Task 3: Save the grouped data to a new Excel sheet
grouped_df.to_excel('C:\\Users\\raduy\\PycharmProjects\\F-score-calculating\\data\\outputdata\\Grouped_F_Score.xlsx', index=False)

# Task 4: Create the list of patterns
ch = ['cb5k', 'cd5k', 'cf5k', 'cm5k', 'cp5k', 'IOR5k', 'IRO5k', 'lp5k', 'OIR5k', 'ORI5k', 'pl5k', 'pm5k', 're5k', 'RIO5k', 'ROI5k', 'rp5k', 'sw5k']

# Task 5: Perform the Wilcoxon test
results = []
for pattern in ch:
    for i in range(0, 10):

        sample1 = filtered_df[filtered_df['Event Log Name'] == f'{pattern}']['F-score']
        sample2 = filtered_df[filtered_df['Event Log Name'] == f'{pattern}_LOGGEN_{i}']['F-score']

        if len(sample1) != 8:
            print(pattern)
        # Check if the samples are identical

        if sample1.equals(sample2):
            continue
        print(f'{pattern}{i}')
        zero_sample_1 = sum(sample1.isin([0]))
        zero_sample_2 = sum(sample2.isin([0]))

        if zero_sample_1 == 8 or zero_sample_2 == 8:
            print('Não é possível aplicar o Wilcoxon')
        else:
            print(f'-------{pattern}  {i}-----------')
            print(sample1)
            print(sample2)
            w, p_value = wilcoxon(sample1, sample2, zero_method='wilcox', alternative = "two-sided",method = "approx")
            results.append((pattern, f'{pattern}', f'{pattern}_LOGGEN_{i}', p_value, w))

    var = None
# Print the results
for result in results:
    if var != result[1] or var == None:
        print('            ')
        print(f'----------------------------------{result[1]}---------------------------------------------------------')
        print('            ')
    if result[3] < 0.05:
        print(f'({result[1]} x {result[2]})-> W:{result[4]} p-value: {result[3]}---Existe diferença')
    elif result[3] > 0.05:
        print(f'({result[1]} x {result[2]})-> W:{result[4]} p-value: {result[3]}--- NÃO Existe diferença')

    var =result[1]

