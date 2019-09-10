def parse_input_file(filename):
    request = {}
    for t in ['EQS','EQP','SUS','SUP','THS','THP','SNS','SNP','PXS','PXP']:
        request[t] = []
    with open(filename, 'r') as infile:
        for line in infile: 
            pick = {}
            pick_line = line.split(',')
            pick['event_type'] = pick_line[0].replace('[','').replace("'",'').strip()
            pick['time'] = pick_line[1].replace("'",'').strip()
            pick['sta'] = pick_line[2].replace("'",'').strip()
            pick['net'] = pick_line[3].replace("'",'').strip()
            pick['loc'] = pick_line[4].replace("'",'').strip()
            pick['chan'] = pick_line[5].replace("'",'').strip()
            pick['pick_type'] = pick_line[6].replace("'",'').strip()
            pick['quality'] = pick_line[7].replace("'",'').strip()
            pick['who'] = pick_line[8].replace(']','').replace("'",'').strip()
            #print(pick) 
            key = "{}{}".format(pick['event_type'], pick['pick_type'])
            print(key)
            request[key].append(pick)
parse_input_file('Labeled_arrivals_from_database.txt')


