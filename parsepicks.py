#$:sed 's/\[//g' Labeled_arrivals_from_database.txt | sed 's/\]//g' | sed "s/'//g" > arrivals.csv

import csv
def parse_input_file(filename):
    request = {}
    for t in ['EQS','EQP','SUS','SUP','THS','THP','SNS','SNP','PXS','PXP']:
        request[t] = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            pick = {}
            pick['event_type'] = row[0].strip()
            pick['time'] = row[1].strip()
            pick['sta'] = row[2].strip()
            pick['net'] = row[3].strip()
            pick['loc'] = row[4].strip()
            pick['chan'] = row[5].strip()
            pick['pick_type'] = row[6].strip()
            pick['quality'] = row[7].strip()
            pick['who'] = row[8].strip()
            #print(pick) 
            key = "{}{}".format(pick['event_type'], pick['pick_type'])
            request[key].append(pick)
    return request

parse_input_file('arrivals.csv')
    