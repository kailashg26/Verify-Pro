
import numpy as np


# Note for Kailash
# all these functions are taken fromm decision/ds_tree
def predict(decTreeModel, input_str):

    input_list = stringtofield(input_str)
    input_array = np.array(input_list)
    input_array = input_array.reshape(1, -1)
    output = decTreeModel.predict(input_array)
    return output[0]


def stringtofield(input):

    List = input.split('/')
    num = len(List)
    packets = []
    for e in List:
        e= e[3:]
        packets.append(e.split(','))
    sizes = [0]*6
    types = []
    for i in range(len(packets)):
        sizes[i]=len(packets[i])
        packet_type = [0]*4
        j = 0
        for each in packets[i]:
            if each.isdigit():
                packet_type[j]=1
            else:
                packet_type[j]=-1
            j+=1
        
        types = types + packet_type
    if(len(types)!=24):
        types= types + [0]*(24-len(types))

    return [num]+sizes+types
