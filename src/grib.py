import math

from sty import fg
from util import cprint

class GribAnalyst:
    def __init__(self, grbs):
        self.grbs = grbs

    def isGrib(self):
      self.grbs
      

    def getInfo(self):
      #cprint(fg.cyan, 'Latlons: ' + self.grbs.latlons())
      print("Info: ")

    def getInventory(self):
        lst = []
        for grb in self.grbs:
            lst.append(grb)
        return lst
    
    # returnds central data within lat1, lat2 and len1, len2 boundaries
    def findCentralData(self, name, lat1, lat2, len1, len2):
        #print('Name: ' + name)
        temp = self.grbs.select(name=name)[0]

        #for t in temp:
        #  cprint(fg.yellow, str(t))

        #print('lats ' + str(lat1) + ' ' + str(lat2) + ' ' + str(len1) + ' ' + str(len2))

        data, lats, lons = temp.data(lat1=lat1,lat2=lat2,lon1=len1,lon2=len2)
        #print('data: ' + str(data))
        #print('lats: ' + str(lats))
        #print('data.shape: ' + str(data.shape))
        zipped = list(zip(data, lats, lons))

        centerIndex = math.ceil((len(zipped) / 2) - 1) 
        selectedData = zipped[centerIndex]

        formatted = {
            "type": name,
            "value": selectedData[0],
            "lat": selectedData[1],
            "lon": selectedData[2]
        }

        return formatted
