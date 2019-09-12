from datetime import datetime
from datetime import timedelta

        
def read_output_to_dict(filename):
    '''Read the output of model into a dictionary keyed on
            key = NET-STA-PICK
    '''
    model_dict = {}
    with open(filename) as f:
        for line in f:
            tmp = line.split()
            key = tmp[0] + "-" + tmp[1] + "-" + tmp[2]
            formatted_time = datetime.strptime(tmp[3], "%Y-%m-%dT%H:%M:%S.%f") # parse str to datetime object
            if key not in model_dict:
                model_dict[key] = []
            model_dict[key].append(formatted_time) 
    return model_dict

out = read_output_to_dict("test.out")
print(out)