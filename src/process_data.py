import csv
import math

with (open("clean_training_data_with_id.csv", newline='') as rf, open("training_clicks.csv", "w", newline='') as wf):
    reader = csv.DictReader(rf)
    writer = csv.DictWriter(wf,
                            ["starting time", "duration", "starting x", "starting y", "movement module",
                             "movement angle", "mouse button", "is abnormal"])
    writer.writeheader()
    dicts = list(reader)
    dicts.sort(key=lambda x: int(x['id']))
    for i in range(0, len(dicts), 2):
        row1 = dicts[i]
        row2 = dicts[i + 1]
        if eval(row1['pressed']) and not eval(row2['pressed']) and row1['button'] == row2['button'] and eval(
                row1['abnormal']) == eval(row2['abnormal']) and float(row1['time']) <= float(row2['time']):
            s_time = float(row1['time'])
            duration = float(row2['time']) - s_time
            s_x = float(row1['x'])
            s_y = float(row1['y'])
            radius = math.hypot(float(row2['x']) - s_x, float(row2['y']) - s_y)
            angle = math.atan2(float(row2['y']) - s_y, float(row2['x']) - s_x)
            button = row1['button']
            abnormality = eval(row1['abnormal'])
            writer.writerow({"starting time": s_time, "duration": duration, "starting x": s_x, "starting y": s_y,
                             "movement module": radius, "movement angle": angle, "mouse button": button,
                             "is abnormal": abnormality})
        else:
            print("mismatch:")
            print(row1)
            print(row2)
