import csv

with open('tofel.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    i = 0
    for row in spamreader:
        i += 1
        print(row[0], row[1])
    print('num: ', i)