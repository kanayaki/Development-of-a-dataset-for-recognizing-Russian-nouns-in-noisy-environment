# скрипт, с помощью которого производилось создание итогового датасета (наложение шумов на записи существительных) и его разметки 

from pydub import AudioSegment
import os
from tqdm import tqdm
import random
import csv


# здесь должны находиться переменные path1, path2 и path3
# в path1 указан путь до папки, из которой скрипт читает аудиофайлы записей существительных, на которые будет производиться наложение
# в path2 указан путь до папки, из которой скрипт читает аудиофайлы записей шумов, которые накладываются на записи существительных
# в path3 указан путь до csv таблицы, в которую будет записана новая разметка получившегося датасета

table = []

for filename1 in tqdm(os.listdir(path1)):
    for filename2 in os.listdir(path2):
        if filename1.endswith('.wav') and filename2.endswith('.wav'):
            sample1 = AudioSegment.from_wav(path1 + filename1)
            sample2 = AudioSegment.from_wav(path2 + filename2)
            random_end = int(len(sample1) / 10 * 6)
            random_a = random.randint(0, random_end)
            random_b = random.randint(0, random_end)
            sample_a = sample1.overlay(sample2, position=random_a)
            sample_b = sample1.overlay(sample2, position=random_b)
            filename1_ = filename1[:-4].split('_')
            filename2_ = filename2[:-4].split('_')
            name_a = f'{filename1_[0]}_{filename2_[0]}_{filename1_[1]}_{filename2_[1]}_a.wav'
            name_b = f'{filename1_[0]}_{filename2_[0]}_{filename1_[1]}_{filename2_[1]}_b.wav'
            speaker = filename1_[0].split('-')[0]
            # следующие две строки стоит раскомментировать и на месте ... указать путь до папки, в которую скрипт будут записывать аудиофайлы
            # папка должна быть создана заранее
            # sample_a.export(f'C.../{name_a}', format='wav')
            # sample_b.export(f'C.../{name_b}', format='wav')
            info_for_table_a = [name_a, speaker, filename1_[1], filename2_[1], len(sample_a), random_a]
            info_for_table_b = [name_b, speaker, filename1_[1], filename2_[1], len(sample_b), random_b]
            table.append(info_for_table_a)
            table.append(info_for_table_b)

with open(path3, "wt", encoding='utf-8') as fp:
    writer = csv.writer(fp, delimiter=",", lineterminator='\n')
    writer.writerow(["filename", "speaker", "noun", "noise", "duration (milliseconds)", "overlay_position"])
    writer.writerows(table)