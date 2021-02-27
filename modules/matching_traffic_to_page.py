import os
import time

start_time = time.time()
source_files_path = '../metas'
traff_file = 'traff.csv'


def prepare_list_of_data_to_match(path: str) -> list:
    file_list = []
    for i in os.listdir(path):
        file_list.append(i)
    return file_list


def make_traffic_dict(filename: str) -> dict:
    traffic_dict = {}
    with open(f'../data_matching/{filename}') as t:
        for i in t:
            url, traff = i.strip().split(',')
            traffic_dict[f'https://kasta.ua{url}'] = traff
    return traffic_dict


traffic_dictionary = make_traffic_dict(traff_file)
files_to_match = prepare_list_of_data_to_match(source_files_path)

for file in files_to_match:
    with open(f'../metas/{file}', encoding='utf-8') as f:
        with open(f'../data_matching/matched_{file}', 'w', encoding='utf-8') as m:
            m.write('URL;Title;H1;Description;Products Quantity;Prod Quantity over 40;Status code;Traffic\n')
            for line in f:
                data_list = line.strip().split(';')
                url = data_list[0]
                if url == 'URL':
                    continue
                try:
                    traff = traffic_dictionary[url]
                    data_list.append(traff)
                except KeyError:
                    continue
                finally:
                    data_string = ';'.join(data_list)
                    m.write(f'{data_string}\n')

                # for key in traffic_dictionary.keys():
                #     if url == key:
                #         data_list.append(data_list[0])



print(f'{time.time() - start_time:.3f}')

