import math

class GribAnalyst:
    def __init__(self, grbs):
        self.grbs = grbs

    def isGrib(self):
      self.grbs
      

    def getInventory(self):
        lst = []
        for grb in self.grbs:
            lst.append(grb)
        return lst
    
    # returnds central data within lat1, lat2 and len1, len2 boundaries
    def findCentralData(self, name, lat1, lat2, len1, len2):
        temp = self.grbs.select(name=name)[0]

        data, lats, lons = temp.data(lat1=lat1,lat2=lat2,lon1=len1,lon2=len2)
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
