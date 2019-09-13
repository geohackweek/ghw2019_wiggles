import csv
import string
import datetime
from datetime import datetime
from datetime import timedelta

# ------------ Parse csv arrivals into separate dirs ------------
etype = ['EQS','EQP','SUS','SUP','THS','THP','SNS','SNP','PXS','PXP']

def parse_input_file(filename):
    request = {}
    for t in etype:
        request[t] = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            line = []
            line.extend([row[3].strip(), row[2].strip(), row[6].strip()])
            formatted_time = datetime.fromtimestamp(float(row[1].strip())).strftime("%Y-%m-%dT%H:%M:%S.%f")
            line.extend([formatted_time, row[7].strip(), row[0].strip()+row[6].strip()])
            key = row[3].strip()
            request[row[0].strip()+row[6].strip()].append(line)
    return request

res = parse_input_file('arrivals.csv')

for ekey in etype:
    with open('parsed_arrivals/' + ekey + '.arrivals.txt', 'w') as f:
        for item in res[ekey]:
            f.write(" ".join(str(it) for it in item) + "\n")
            