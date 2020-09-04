import csv
import sys

csv.field_size_limit(sys.maxsize)
fin = open('train1.csv','r')
fout = open('train.csv','w')
reader = csv.reader(fin)
writer = csv.writer(fout)
count = 0
for line in reader:
    count =count + 1
    per = count/9517039
    if count%1000000 is 0:
        print(per)
    line1 = line[:3]
    writer.writerow(line1)