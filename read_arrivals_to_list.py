import csv

def read_arrivals_to_list(filename):
    '''Read arrivals csv file and stuff into 2-dim array'''
    
    model_list = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            model_list.append(row)
    return model_list

out = read_arrivals_to_list("arrivals.csv")
print(out)