import os
import constants

rootdir = os.getcwd() + "/xml_modified_logs/"
gestureList = constants.GESTURE_LIST

for directory in os.listdir(rootdir):
    user = os.path.join(rootdir, directory)
    for fileName in os.listdir(user):
        # print(fileName)    
        data = None
        with open(os.path.join(user,fileName), 'r', encoding='utf-8') as file:
            data = file.readlines()
        for i in range(len(data)):
            for gesture in gestureList:
                data[i] = data[i].replace('--','hyphen-')
                data[i] = data[i].replace('1-','one-')
                data[i] = data[i].replace('2-','two-')
                data[i] = data[i].replace('3-','three-')
                data[i] = data[i].replace('4-','four-')
                data[i] = data[i].replace('5-','five-')
                data[i] = data[i].replace('6-','six-')
                data[i] = data[i].replace('7-','seven-')
                data[i] = data[i].replace('8-','eight-')
                data[i] = data[i].replace('9-','nine-')
                data[i] = data[i].replace('0-','zero-')
                data[i] = data[i].replace('-','0')
                data[i] = data[i].replace('010','10')
                data[i] = data[i].replace('X011','X01')
        with open(os.path.join(user,fileName), 'w', encoding='utf-8') as file:
            file.writelines(data)