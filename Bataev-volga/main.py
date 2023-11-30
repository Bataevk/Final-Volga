from functions import *
import matplotlib.pyplot as plt
from random import randint


data = extract_dataFrame("task.csv")
data = data.sort_values(by='longitude', ascending=True)

ic(data.info())

all_count_devices = sum(data['end_devices_count'])
ic(all_count_devices)

MAX_COUNT_BS = 1000
MIN_PS = 0.95


bs_layer= [None for _ in range(len(data['latitude']))] #null
home_indexes = [i for i in range(len(bs_layer))]

first_layer = [bs_layer, home_indexes]

def generation_step(data, last_layer, count_states = 10, count_changes = 10):
    global all_count_devices

    temp_array = [None for _ in range(count_states)]

    layer = pd.DataFrame({
        'generations_layer': temp_array,
        'grades-1': temp_array,
        'grades-2': temp_array,
    })

    for i in range(count_states):
        layer['generations_layer'][i] = [list(last_layer[0][:]), list(last_layer[1][:])]

        for _ in range(count_changes):
            rand_index = randint(0,len(layer['generations_layer'][i] [0]) - 1)
            layer['generations_layer'][i] [0] [rand_index] = randint(0,len(bs)-2)

        layer['grades-1'][i], layer['grades-2'][i] = get_grade(data, layer['generations_layer'][i] [0], all_count_devices)


    return layer


def generation_while(data,last_layer):
    global MAX_COUNT_BS, MIN_PS

    last_grade = 0
    while (len(last_layer[0]) - last_layer[0].count(None)) < MAX_COUNT_BS:
        current_layers = generation_step(data, last_layer, count_changes = 50, count_states = 1000)

        current_layers.sort_values(by='grades-1', ascending=False)
        ic.enable()

        ic(current_layers['grades-1'][0], current_layers['grades-2'][0])
        
        last_layer = current_layers['generations_layer'][0]
        last_grade = current_layers['grades-1'][0]

        for i in range(len(current_layers['generations_layer'])):
            if current_layers['grades-1'][i] >= MIN_PS:
                return current_layers['generations_layer'][i]
        ic((len(last_layer[0]) - last_layer[0].count(None)))
        ic.disable()
    print("Last grade :", last_grade)
    return last_layer


# ic.disable()
# grades = (
#     get_grade(data, bs_layer, all_count_devices),
#     get_grade(data, bs_layer, all_count_devices)
# )

# ic.enable()
# ic(grades, sum(data['end_devices_count']))

ic(len(first_layer[0]), len(first_layer[1]))
ic.disable()
# first_step = generation_step(data, first_layer).sort_values(by='grades-2', ascending=True)
# ic(first_step['grades-1'], first_step['grades-2'])

result = generation_while(data, first_layer)
ic.enable()

out_array = [[],[]]

for i in range(len( result[0])):
    if result[0][i] is not None:
        out_array[0].append(data['house_uuid'][result[1][i]])
        out_array[1].append(bs[result[0][i]].type)

out_data = pd.DataFrame({
    'house_uuid': out_array[0],
    'type': out_array[1],
})
out_data.dropna()
save_csv(out_data, 'result.csv')



# plt.plot(data['latitude'], data['longitude'], 'o')
# plt.show()