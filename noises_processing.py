# скрипт, с помощью которого производилось переименование записей шумов, их обрезка и переработка связанной с ними разметки

from pydub import AudioSegment, silence
import os
from tqdm import tqdm
import csv

# здесь должны находиться переменные path1, path2 и path3
# в path1 указан путь до папки, из которой скрипт читает аудиофайлы
# в path2 указан путь до csv таблицы, в которой содержится вариант разметки исходного датасета со звуками окружающей природы
# она содержит соответствия имен файлов и категорий звуков
# в path3 указан путь до csv таблицы, в которую будет записана новая разметка получившегося датасета

with open(path2) as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    next(reader, None)
    table = [row for row in reader]


for filename in tqdm(os.listdir(path1)):
    sample = AudioSegment.from_wav(path1 + filename)
    si = silence.detect_leading_silence(sample, silence_threshold=-35, chunk_size=1)
    for i in range(len(table)):
        if table[i][0] == filename:
            sound_name = table[i][1].replace('_', '-')
            table[i][1] = sound_name
            table[i][0] = table[i][0][:-4] + '_' + sound_name + '.wav'
            table[i].append(len(sample[si:]))
    if si == 5000:
        print(filename, len(sample[si:]))
    # следующую строку стоит раскомментировать и на месте ... указать путь до папки, в которую скрипт будут записывать аудиофайлы
    # папка должна быть создана заранее
    # sample[si:].export(f'.../{filename[:-4]}_{sound_name}.wav', format='wav')

with open(path3, "wt") as fp:
    writer = csv.writer(fp, delimiter=",", lineterminator='\n')
    writer.writerow(["filename", "category", "duration (milliseconds)"])
    writer.writerows(table)