import pandas as pd 
import numpy as np
from icecream import ic
from geopy.distance import geodesic
from geopy import Point


# БС-1 (type=1).
#     Радиус: 1 км.
#     Макс. количество подключаемых квартир: 2000.
#     Стоимость: 50 000 руб.
# БС-2 (type=2).
#     Радиус: 2 км.
#     Макс. количество подключаемых квартир: 10000.
#     Стоимость: 180 000 руб.

class bs:
    def __init__(self, radius, max_count_devices, cost, type):
        self.type = type
        self.radius = radius
        self.max_count_devices = max_count_devices
        self.cost = cost

bs = [
    bs(1,2000, 50_000, 1),
    bs(2,10000, 180_000, 2),
    None
]



def get_count_bs(data, bs, bs_i, end_devices_count,):
    def help_for(a,b,step = 1):
        count_devices = 0
        for i in range(a,b,step):
            if geodesic(
                Point(0, data['longitude'][bs_i]),
                Point(0, data['longitude'][i])
                ).km > bs.radius: return count_devices
            distance = geodesic(
                Point(data['latitude'][bs_i], data['longitude'][bs_i]),
                Point(data['latitude'][i], data['longitude'][i])
                ).km
            if distance <= bs.radius:
                if  count_devices + end_devices_count[i] > bs.max_count_devices:
                    end_devices_count[i] = end_devices_count[i] + count_devices - bs.max_count_devices 
                    return bs.max_count_devices
                count_devices += end_devices_count[i]
                end_devices_count[i] = 0
        return count_devices

    return help_for(bs_i, len(data['latitude']), step = 1) + help_for(bs_i-1, -1, step = -1)

    return count_devices

def get_grade(data, column_bs, all_count_devices):
    global bs
    count_devices = 0
    end_devices_count = list(data['end_devices_count'])


    for i in range(len(column_bs)):
        ic(int(i/len(column_bs)*1000)/10,"%")
        if column_bs[i] is not None:
            count_devices += get_count_bs(data, bs[column_bs[i]], i, end_devices_count)

    cost_bss = sum([
        (bs[i].cost if i is not None else 0) for i in column_bs
        ])
    
    return count_devices/all_count_devices, cost_bss


def extract_dataFrame(name: str):
    return pd.read_csv(name, sep = ';')

def save_csv(data, name: str):
    data.to_csv(name, sep = ';', index = False)