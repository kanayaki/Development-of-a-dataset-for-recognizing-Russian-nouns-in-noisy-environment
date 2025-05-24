# скрипт, с помощью которого производилось переименование записей существительных и переработка связанной с ними разметки


from pydub import AudioSegment
import os
from tqdm import tqdm
import csv

# здесь должны находиться переменные path1, path2 и path3
# в path1 указан путь до папки, из которой скрипт читает аудиофайлы
# в path2 указан путь до csv таблицы, в которой содержится вариант разметки исходного датасета с записями существительных
# она содержит соответствия имен файлов и слов, произносимых информантом
# таблица должна содержать данные только об аудиозаписях, находящихся в читаемой папке
# в path3 указан путь до csv таблицы, в которую будет записана новая разметка получившегося датасета

path2 = 'C:/Users/Эля/Desktop/sound_datasets/fa1-fy4/fy3/table_old.csv'
path3 = 'C:/Users/Эля/Desktop/sound_datasets/fa1-fy4/fy3/table.csv'

with open(path2, encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    next(reader, None)
    table = [row for row in reader]

for filename in tqdm(os.listdir(path1)):
    if filename.endswith('.wav'):
        sample = AudioSegment.from_wav(path1 + filename)
        for i in range(len(table)):
            if table[i][0] == filename:
                new_filename = table[i][0][:-4] + '_' + table[i][1] + '.wav'
                table[i][0] = new_filename
                table[i].append(len(sample))
                # следующую строку стоит раскомментировать и на месте ... указать путь до папки, из которой скрипт читает аудиофайлы
                # os.rename(f'.../{filename}', f'.../{new_filename}')
                break

with open(path3, "wt", encoding='utf-8') as fp:
    writer = csv.writer(fp, delimiter=",", lineterminator='\n')
    writer.writerow(["filename", "word", "duration (milliseconds)"])
    writer.writerows(table)