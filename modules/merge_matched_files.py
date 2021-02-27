import os

files = os.listdir('../data_matching')
files.remove('traff.csv')

with open('../merged/merged_file.txt', 'w', encoding='utf-8') as m:
    m.write('URL;Title;H1;Description;Products Quantity;Prod Quantity over 40;Status code;Traffic\n')
    for file in files:
        with open(f'../data_matching/{file}', encoding='utf-8') as f:
            for line in f:
                if line.startswith('URL;'):
                    continue
                m.write(line)

