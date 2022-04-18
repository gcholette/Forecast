import pygrib
import requests
import arrow
from os.path import exists

from constants import hrdps_path
from grib import GribAnalyst
from file_manager import FileManager

class HRDPSManager:
    def __init__(self, hours=0, variables=["TMP_TGL_2"]):
        self.rangeTop = hours
        self.variables = variables

    def loadGribFiles(self):
        print ("Requesting GRIB2 CMC HRDPS files...")
        lst = HRDPSFileListGenerator().generateUrlList(rangeTop=self.rangeTop, variables=self.variables)
        print("Url list:" + str(lst))
        FileManager.deleteAllFiles()
        FileManager.createMissingFiles()

        for url in lst:
            r = requests.get(url=url)
            status = r.status_code
            if (status == 200): 
              FileManager.addHRDPSFile("CMC_hrdps" + url.split("CMC_hrdps")[1], r.content)
            else:
              print("Recevied status code " + str(status) + " while fetching HRDPS GRIB2 file.")

        print ("Done.")

    def loadData(self):
        print ("Loading data...")
        lat = 45.541092
        lon = -73.494955
        lst = HRDPSFileListGenerator().generateFilenameList(rangeTop=self.rangeTop, variables=self.variables)

        data = []
        for filename in lst:
            file_path = hrdps_path + filename
            if (exists(file_path)): 
                grbs = pygrib.open(hrdps_path + filename)
                timestamp = HRDPSFilenameFormatter.getTimestampFromFilename(filename)
                #attr = '2 metre temperature'
                gribAnalyst = GribAnalyst(grbs)
                inv1 = gribAnalyst.getInventory()
                print(str(inv1))
                inv = str(inv1[0])
                if (len(inv) > 0):
                    attr = inv.split(':')[1]
                    localData = gribAnalyst.findCentralData(attr, lat-0.02, lat+0.02, lon-0.02, lon+0.02)
                    localData['time'] = timestamp
                    data.append(localData)
            else:
              print("No file to load.")

        print ("Done.")
        return data

#  CMC_hrdps_domain_Variable_LevelType_level_ps2.5km_YYYYMMDDHH_Phhh-mm.grib2
#  Variable examples https://weather.gc.ca/grib/HRDPS_HR/HRDPS_nat_ps2p5km_P000_deterministic_e.html
class HRDPSFilenameFormatter:
    def __init__(self, type="hrdps", domain="east", variable="TMP_TGL_2", startDate=arrow.utcnow().format(), resolution='ps2.5km', hour=0):
        self.type = type
        self.domain = domain
        self.variable = variable
        self.startDate = arrow.get(startDate).format('YYYYMMDD18')
        self.resolution = resolution
        self.hour = '%03d' % hour

    def formatFilename(self):
        #  CMC_hrdps_domain_Variable_LevelType_level_ps2.5km_YYYYMMDDHH_Phhh-mm.grib2
        fileName = "CMC_%s_%s_%s_%s_%s_P%s-00.grib2" % (self.type, self.domain, self.variable, self.resolution, self.startDate, self.hour)
        return fileName

    def formatFullPath(self):
        #  CMC_hrdps_domain_Variable_LevelType_level_ps2.5km_YYYYMMDDHH_Phhh-mm.grib2
        urlBase = 'https://dd.weather.gc.ca/model_hrdps/east/grib2/18/'
        fileName = "%s%s/%s" % (urlBase, self.hour, self.formatFilename())
        return fileName
        
    @staticmethod
    def getTimestampFromFilename(filename): 
        a = filename.split('_')
        date = a[len(a)-2]
        hour = a[len(a)-1][2:4]
        time = arrow.get(date, 'YYYYMMDD18').shift(hours=int(hour)).format()
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
        urlBase = 'https://dd.weather.gc.ca/model_hrdps/east/grib2/18/'
        for variable in variables:
            for hour in range(0, rangeTop):
                hrdpsff = HRDPSFilenameFormatter(startDate=arrow.utcnow().to('-04:00').format(), hour=hour, variable=variable)
                filename = urlBase + ( '%03d/' % hour ) + hrdpsff.formatFilename()
                names.append(filename)
        return names