import pandas as pd
import re

def pregunta_01():
    with open('./files/input/clusters_report.txt', 'r') as file:
        lines = file.readlines()

    data_start_index = next(i for i, line in enumerate(lines) if "---" in line) + 1
    columns_line = lines[data_start_index - 2]
    normalized_columns = ['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave']

    data_lines = lines[data_start_index:]
    data = []
    temp_row = None
    for line in data_lines:
        if re.match(r'\s*\d+\s', line):
            if temp_row:
                temp_row[3] = ' '.join(temp_row[3]).replace('\n', ' ').strip()
                temp_row[3] = re.sub(r'\s{2,}', ' ', temp_row[3])
                temp_row[3] = temp_row[3].rstrip('.')
                data.append(temp_row)
            split_line = re.split(r'\s{2,}', line.strip(), maxsplit=3)
            temp_row = [split_line[0], split_line[1], split_line[2], [split_line[3]]]
        else:
            if temp_row:
                temp_row[3].append(line.strip())

    if temp_row:
        temp_row[3] = ' '.join(temp_row[3]).replace('\n', ' ').strip()
        temp_row[3] = re.sub(r'\s{2,}', ' ', temp_row[3])
        temp_row[3] = temp_row[3].rstrip('.')
        data.append(temp_row)

    for row in data:
        row[3] = re.sub(r',\s+', ', ', row[3])

    df = pd.DataFrame(data, columns=normalized_columns)
    df['cluster'] = df['cluster'].astype(int)
    df['cantidad_de_palabras_clave'] = df['cantidad_de_palabras_clave'].astype(int)
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].str.replace(',', '.').str.rstrip('%').astype(float)

    return df

if __name__ == "__main__":
    print(pregunta_01())
