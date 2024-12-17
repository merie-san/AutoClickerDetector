with open("clean_training_data.csv", "r") as f, open("clean_training_data_with_id.csv", "w") as f1:
    i = 0
    for line in f:
        if i == 0:
            f1.write("id," + line)
        else:
            f1.write(str(i - 1) + "," + line)
        i += 1
