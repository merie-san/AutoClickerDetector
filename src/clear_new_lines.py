with open("training_data.csv", "r") as f, open("clean_training_data.csv", "w") as f1:
    for line in f:
        if line.strip():
            f1.write(line)
