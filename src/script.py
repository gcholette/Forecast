import pygrib
import math
import shutil
import arrow
import datetime
import requests
import json 
import os
from functools import reduce

data_path = '/app/data/'
hrdps_path = '/app/data/cmc/hrdps/'

# En Kelvin
temperature_variables = ["TMP_TGL_2", "TMP_TGL_40", "TMP_ISBL_1015", "TMP_ISBL_1000"]

# humidité spécifique en kg kg-1
humidity_variables = ["SPFH_TGL_2", "SPFH_TGL_40", "SPFH_ISBL_1015", "SPFH_ISBL_0985"]

# precipitable water in kg m-2
precipitation_variables = ["PWAT_EATM_0", "CWAT_EATM_0"]

# wind speed in m/sec
wind_variables = ["WDIR_TGL_10", "WIND_TGL_10"]


#  CMC_hrdps_domain_Variable_LevelType_level_ps2.5km_YYYYMMDDHH_Phhh-mm.grib2
#  Variable examples https://weather.gc.ca/grib/HRDPS_HR/HRDPS_nat_ps2p5km_P000_deterministic_e.html
class HRDPSFilenameFormatter:
    def __init__(self, type="hrdps", domain="east", variable="TMP_TGL_2", startDate=arrow.utcnow().format(), resolution='ps2.5km', hour=0):
        self.type = type
        self.domain = domain
        self.variable = variable
        self.startDate = arrow.get(startDate).format('YYYYMMDD00')
        self.resolution = resolution
        self.hour = '%03d' % hour

    def formatFilename(self):
        #  CMC_hrdps_domain_Variable_LevelType_level_ps2.5km_YYYYMMDDHH_Phhh-mm.grib2
        fileName = "CMC_%s_%s_%s_%s_%s_P%s-00.grib2" % (self.type, self.domain, self.variable, self.resolution, self.startDate, self.hour)
        return fileName

    def formatFullPath(self):
        #  CMC_hrdps_domain_Variable_LevelType_level_ps2.5km_YYYYMMDDHH_Phhh-mm.grib2
        urlBase = 'https://dd.weather.gc.ca/model_hrdps/east/grib2/00/'
        fileName = "%s%s/%s" % (urlBase, self.hour, self.formatFilename())
        return fileName
        
    @staticmethod
    def getTimestampFromFilename(filename): 
        a = filename.split('_')
        date = a[len(a)-2]
        hour = a[len(a)-1][2:4]
        time = arrow.get(date, 'YYYYMMDD00').shift(hours=int(hour)).format()
        return time

        
class HRDPSFileListGenerator:
    def generateFilenameList(self, rangeTop=0, variables=["TMP_TGL_2"]):
        names = []
        for variable in variables:
            for hour in range(0, rangeTop):
                hrdpsff = HRDPSFilenameFormatter(startDate=arrow.utcnow().to('-04:00').format(), hour=hour, variable=variable)
                filename = hrdpsff.formatFilename()
                names.append(filename)
        return names
    
    def generateUrlList(self, rangeTop=0, variables=["TMP_TGL_2"]):
        names = []
        urlBase = 'https://dd.weather.gc.ca/model_hrdps/east/grib2/00/'
        for variable in variables:
            for hour in range(0, rangeTop):
                hrdpsff = HRDPSFilenameFormatter(startDate=arrow.utcnow().to('-04:00').format(), hour=hour, variable=variable)
                filename = urlBase + ( '%03d/' % hour ) + hrdpsff.formatFilename()
                names.append(filename)
        return names
    

class GribFileFetcher:
    def fetch(self, url):
        r = requests.get(url=url) 
        data = r.json() 
        print(str(data))
    

class GribAnalyst:
    def __init__(self, grbs):
        self.grbs = grbs

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

class GribFileManager:
    def createMissingFiles(self):
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        if not os.path.exists(data_path + 'cmc/'):
            os.mkdir(data_path + 'cmc/')
        if not os.path.exists(hrdps_path):
            os.mkdir(hrdps_path)

    def deleteAllFiles(self):
        if os.path.exists(data_path):
            shutil.rmtree(data_path + 'cmc')
    
    def addHRDPSFile(self, filename, content): 
        self.createMissingFiles()
        path = data_path + 'cmc/hrdps/'
        with open(path + filename, 'wb') as f:
            f.write(content)


class HRDPSManager:
    def __init__(self, hours=0, variables=["TMP_TGL_2"]):
        self.rangeTop = hours
        self.variables = variables

    def loadGribFiles(self):
        print ("Requesting Grib CMC HRDPS files...")
        lst = HRDPSFileListGenerator().generateUrlList(rangeTop=self.rangeTop, variables=self.variables)
        gribFileManager = GribFileManager()
        gribFileManager.deleteAllFiles()

        for url in lst:
            r = requests.get(url=url)
            gribFileManager = GribFileManager()
            gribFileManager.addHRDPSFile("CMC_hrdps" + url.split("CMC_hrdps")[1], r.content)

        print ("Done.")

    def loadData(self):
        print ("Loading data...")
        lat = 45.541092
        lon = -73.494955
        lst = HRDPSFileListGenerator().generateFilenameList(rangeTop=self.rangeTop, variables=self.variables)

        data = []
        for filename in lst:
            grbs = pygrib.open(hrdps_path + filename)
            timestamp = HRDPSFilenameFormatter.getTimestampFromFilename(filename)
            #attr = '2 metre temperature'
            gribAnalyst = GribAnalyst(grbs)
            inv = str(gribAnalyst.getInventory()[0])
            if (len(inv) > 0):
                attr = inv.split(':')[1]
                localData = gribAnalyst.findCentralData(attr, lat-0.02, lat+0.02, lon-0.02, lon+0.02)
                localData['time'] = timestamp
                data.append(localData)

        print ("Done.")
        return data
 
def main():
    hrdps = HRDPSManager(hours=40, variables=["TMP_TGL_2" ,"SPFH_TGL_2"])
    #hrdps.loadGribFiles()
    data = hrdps.loadData()
    for x in data:
        print (str(x))

if __name__ == "__main__":
    main()