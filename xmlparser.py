#Authors - Harsh Athavale & Abdul Samadh Azath

import os
import xml.etree.ElementTree as ET
from constants import GESTURE_LIST

class Parser():
    def __init__(self):
        self.offline_data = {}
        rootdir = os.getcwd() + "/mmg/"
        for directory in os.listdir(rootdir):
            user = os.path.join(rootdir, directory)
            userName = user.split("/")[-1]
            # print(userName)
            if os.path.isdir(user):
                self.offline_data[userName] = {}
                # for speed in os.listdir(user):
                #     self.offline_data[userName][speed] = {}
                c=0
                itrcount=0
                

                sorted_files = sorted(os.listdir(user))
            # print(sorted_files)
                    
            # for files in sorted_files:
            #     print(files)


                for fileName in sorted_files:
                    # print(fileName)
                    c+=1
                    if c%10 == 0 :
                        itrcount+=1

                    # gestureName = fileName[0]
                    gestureName = fileName.split('-')[3]
                    if gestureName == 'd':
                        gestureName='/'
                    
                    # print(gestureName)
                    # itrname = self.getCleanedFileName(fileName)
                    itrname = str((c-(itrcount*10))%10)
                    # print(itrname)
                    if gestureName in self.offline_data[userName]:
                        # self.offline_data[userName][gestureName][itrname]=[]
                        self.offline_data[userName][gestureName][itrname]=self.getCoordinatesFromXML(user + "/" + fileName)
                    else:
                        self.offline_data[userName][gestureName]={}
                        # self.offline_data[userName][gestureName][itrname]=[]
                        self.offline_data[userName][gestureName][itrname]=self.getCoordinatesFromXML(user + "/" + fileName)
            #print(self.offline_data)
        
                # print(c)
    def getCoordinatesFromXML(self, fileLocation):
        points = []
        root = ET.parse(fileLocation).getroot()
        for stroke in root:
            tempstroke=[]
            for point in stroke:
                tempstroke.append([int(point.attrib['X']), int(point.attrib['Y'])])
                # tempstroke.append(Point(int(point.attrib['X']), int(point.attrib['Y'])))
            points.append(tempstroke)
            
        return points
    
    def getCleanedFileName(self, fileName):
        fileName = fileName.replace(".xml", "")
        res = fileName
        # res = "".join(filter(lambda x: not x.isdigit(), fileName))
        return res

    def getOfflineData(self):
        return self.offline_data