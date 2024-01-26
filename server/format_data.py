import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import rgb2hex
from matplotlib.colors import ListedColormap
import numpy as np
import datetime

def formatChartData(labels, data, color, chartType='bar', data_type="time", group_labels = []):
    '''
    labels: list of string labels
    data: list of values
    data_type can be "time" or "percent"
    color_labels is used to group labels. For hint usage, color_labels is the hint classification
    '''
    chartData = {
        'datasets': [],
        'labels': [],
        'backgroundColors': []  
    }

    if group_labels:
        labels = np.array(labels, dtype=str)
        group_labels = np.array(group_labels, dtype=str)
        labels = np.char.add(np.array([" - " for i in range(len(labels))], dtype=str), labels)
        labels = np.char.add(group_labels, labels)

    len_data = len(data)

    cmap = cm.get_cmap('viridis', len_data)
    newcmp = ListedColormap(cmap(np.linspace(0.4, 1.2, len_data)))

    # Create colors
    for i in range(newcmp.N):
        rgba = newcmp(i)
        # chartData['backgroundColors'].append(rgb2hex(rgba))
        chartData['backgroundColors'].append('5944c2')
    
    has_zones = False
    zone_labels = []

    for i, label in enumerate(labels):
        idx = label.lower().find("-") # -1 if no zones detected
        dataset_index = -1 # index of the dataset to append the data to. Changes only if zones are detected

        if idx != -1: # zone detected
            
            zone_label = label[:idx].lower().strip()

            # new zone detected
            if zone_label not in zone_labels:
                zone_labels.append(zone_label)
                addEmptyDataSet(chartData['datasets'])
                chartData['datasets'][-1]['label'] = zone_label
                chartData['datasets'][-1]['backgroundColor'] =  chartData['backgroundColors'][len(zone_labels)-1]

            # zone already detected
            else:
                dataset_index = zone_labels.index(zone_label)

            chartData['labels'].append(label[idx+2:])


        else: # no zones
            chartData['labels'].append(label)
            if chartData['datasets'] == []:

                addEmptyDataSet(chartData['datasets'])
                chartData['datasets'][-1]['backgroundColor'] =  chartData['backgroundColors'][i]

        chartData['datasets'][dataset_index]['data'].append(data[i])
        chartData['datasets'][dataset_index]['labels'].append(chartData['labels'][-1])

    # if zones are detected, create a dataset with the average of each zone
    has_zones = len(chartData['datasets']) >= 2
    globalChartData = {}
    if has_zones:
        globalChartData = {
            'datasets': [],
            'labels': [],
            'backgroundColors': []
        }
        for dataset in chartData['datasets']:
            if data_type == "time":
                global_data_value =sum(dataset['data'])
            elif data_type == "percent":
                global_data_value = sum(dataset['data'])/len(dataset['data'])
            
            globalChartData['datasets'].append({
                'data': [global_data_value],
                'label': dataset['label'],
                'labels': dataset['label'],
                'visible': 'true',
                'backgroundColor': dataset['backgroundColor']
            })
            globalChartData['labels'].append(dataset['label'])
            globalChartData['backgroundColors'].append(dataset['backgroundColor'])

    list_num_colors = [i for i in range(2*len(chartData['datasets']))]
    norm = plt.Normalize()
    colors = newcmp(norm(list_num_colors))

    hex_colors = [color] * len(colors)
    chartData['backgroundColors'] = hex_colors
    for i, dataset in enumerate(chartData['datasets']):
        dataset['backgroundColor'] = hex_colors[i]

    return {
        'title':"",
        'hasZones': has_zones,
        'detailedChartData': {'chartData':chartData},
        'globalChartData': {'chartData':globalChartData},
        'chartType': chartType,
    }

def addEmptyDataSet(datasets):
    datasets.append({
        'data':[],
        'label': '',
        'labels':[],
        'visible': 'true',
        'backgroundColor': ''
    })


def deltaTimeToString(duration): # duration is a datetime.timedelta object
    if duration==None or duration==0:
        return "0s"
    if type(duration) == float:
        seconds = int(duration)
    if type(duration) == datetime.timedelta:
        seconds = duration.total_seconds()

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int((seconds % 60))
    
    if hours > 0:
        return str(hours) + "h " + str(minutes) + "m "
    elif minutes > 0:
        return str(minutes) + "m " + str(seconds) + "s"
    else:
        return str(seconds) + "s"

def reformatDate(str_date):
    # str_date is in the format yyyy-mm-dd
    # we need to reformat it to yyyy:mm:dd 00:00:00
    return datetime.datetime.strptime(str_date, "%Y-%m-%d")
    # return str_date + " 00:00:00"