import csv
import math
from math import atan2

with (open("training_clicks.csv", newline='') as rf, open("training_batch.csv", "w", newline='') as wf):
    reader = csv.DictReader(rf)
    writer = csv.DictWriter(wf,
                            ["mean ttnc", "std ttnc", "mean duration", "std duration", "mean x", "mean y",
                             "std x", "std y", "mean mov module", "mean mov angle", "std mov module", "std mov angle",
                             "mean in-click module", "std in-click module", "mean in-click angle", "std in-click angle",
                             "left click ratio", "abnormal activity"])
    writer.writeheader()
    dicts = list(reader)
    dicts.sort(key=lambda x: float(x['starting time']))
    for i in range(len(dicts) - 10):

        TTNC = []
        mouse_mov_x = []
        mouse_mov_y = []
        mouse_mov_r = []
        mouse_mov_a = []
        mean_dur = 0
        mean_x = 0
        mean_y = 0
        mean_r = 0
        mean_a = 0
        left_ratio = 0
        n_abnormal = 0

        for j in range(10):
            TTNC.append(float(dicts[j + i + 1]['starting time']) - float(dicts[j + i]['starting time']))
            mouse_mov_x.append(float(dicts[j + i + 1]['starting x']) - float(dicts[j + i]['starting x']))
            mouse_mov_y.append(float(dicts[j + i + 1]['starting y']) - float(dicts[j + i]['starting y']))
            mouse_mov_r.append(math.hypot(mouse_mov_x[j], mouse_mov_y[j]))
            mouse_mov_a.append(math.atan2(mouse_mov_y[j], mouse_mov_x[j]))
            mean_dur += float(dicts[j + i]['duration'])
            mean_x += float(dicts[j + i]['starting x'])
            mean_y += float(dicts[j + i]['starting y'])
            mean_r += float(dicts[j + i]['movement module'])
            mean_a += float(dicts[j + i]['movement angle'])
            if dicts[j + i]['mouse button'] == 'Button.left':
                left_ratio += 1
            if dicts[j + i]['is abnormal'] == 'True':
                n_abnormal += 1

        mean_mov_x = sum(mouse_mov_x) / len(mouse_mov_x)
        mean_mov_y = sum(mouse_mov_y) / len(mouse_mov_y)
        mean_mov_r = math.hypot(mean_mov_x, mean_mov_y)
        mean_mov_a = math.atan2(mean_mov_y, mean_mov_x)
        mean_TTNC = sum(TTNC) / len(TTNC)
        mean_dur = mean_dur / 10
        mean_x = mean_x / 10
        mean_y = mean_y / 10
        mean_r = mean_r / 10
        mean_a = mean_a / 10
        left_ratio = left_ratio / 10
        abnormal = n_abnormal >= 5

        std_TTNC = 0
        std_dur = 0
        std_x = 0
        std_y = 0
        std_mov_r = 0
        std_mov_a = 0
        std_r = 0
        std_a = 0

        for j in range(len(TTNC)):
            std_TTNC += (TTNC[j] - mean_TTNC) ** 2
            std_mov_r += (mouse_mov_r[j] - mean_mov_r) ** 2
            std_mov_a += (mouse_mov_a[j] - mean_mov_a) ** 2
            std_dur += (float(dicts[j + i]['duration']) - mean_dur) ** 2
            std_x += (float(dicts[j + i]['starting x']) - mean_x) ** 2
            std_y += (float(dicts[j + i]['starting y']) - mean_y) ** 2
            std_r += (float(dicts[j + i]['movement module']) - mean_r) ** 2
            std_a += (float(dicts[j + i]['movement angle']) - mean_a) ** 2

        std_TTNC = math.sqrt(std_TTNC / len(TTNC))
        std_mov_r = math.sqrt(std_mov_r / len(mouse_mov_r))
        std_mov_a = math.sqrt(std_mov_a / len(mouse_mov_a))
        std_dur = math.sqrt(std_dur / 10)
        std_x = math.sqrt(std_x / 10)
        std_y = math.sqrt(std_y / 10)
        std_r = math.sqrt(std_r / 10)
        std_a = math.sqrt(std_a / 10)
        writer.writerow(
            {"mean ttnc": mean_TTNC, "std ttnc": std_TTNC, "mean duration": mean_dur, "std duration": std_dur,
             "mean x": mean_x, "mean y": mean_y, "std x": std_x, "std y": std_y, "mean mov module": mean_mov_r,
             "mean mov angle": mean_mov_a, "std mov module": std_mov_r, "std mov angle": std_mov_a,
             "mean in-click module": mean_r, "std in-click module": std_r, "mean in-click angle": mean_a,
             "std in-click angle": std_a, "left click ratio": left_ratio, "abnormal activity": abnormal})
