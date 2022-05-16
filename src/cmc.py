from ast import For
import arrow
import requests
import pygrib

from sty import fg
from os.path import exists
from constants import hrdps_path
from grib import GribAnalyst
from file_manager import FileManager
from util import cprint

class CMC:
    def __init__(self, cmc_type, domain='east', resolution='ps2.5km', variables=[], run_hour = '00', range_top = 48):
        self.type = cmc_type
        self.domain = domain
        self.resolution = resolution
        self.variables = variables
        self.run_hour = run_hour
        self.range_top = range_top

    def fetchFiles(self, urls, files):
        needToFetch = False
        for file in files:
          if not FileManager.fileExists(file):
            needToFetch = True
        
        if not needToFetch:
          return ''

        FileManager.deleteAllFiles()
        FileManager.createMissingFiles()

        for url in urls:
            r = requests.get(url=url)
            status = r.status_code
            if (status == 200):
              match self.type:
                case 'hrdps':
                  FileManager.addHRDPSFile("CMC_hrdps" + url.split("CMC_hrdps")[1], r.content)
                case 'default':
                  cprint(fg.red, 'Not implemented')
            else:
              cprint(fg.red, "Recevied status code " + str(status) + " while fetching HRDPS GRIB2 file.")

    def loadGribFromFiles(self, lat, lon, filePaths = []):
      match self.type:
        case 'hrdps':
          diff = 0.02
          data = []
          for filename in filePaths:
              file_path = hrdps_path + filename
              if (exists(file_path)): 
                  grbs = pygrib.open(hrdps_path + filename)
                  timestamp = FileManager.getTimestampFromFilename(filename)
                  gribAnalyst = GribAnalyst(grbs)
                  inv1 = gribAnalyst.getInventory()
                  inv = str(inv1[0])
                  if (len(inv) > 0):
                      attr = inv.split(':')[1]
                      localData = gribAnalyst.findCentralData(attr, lat-diff, lat+diff, lon-diff, lon+diff)
                      localData['time'] = timestamp
                      localData['time'] = arrow.get(localData['time']).to('-04:00').shift(hours=int(self.run_hour)).format()
                      if (localData['type'] == '2 metre temperature'):
                        localData['value'] = round(localData['value'] - 273.15, 2)
                      data.append(localData)
              else:
                cprint(fg.red, "No file to load.")

          return data
        case 'default':
          cprint(fg.red, 'Not implemented')
          return []
      cprint(fg.yellow, self.type)

    def formatFilename(self, startDate, forecastHour, variable):
        formatedHour = '%03d' % self.typeMultiplier(forecastHour)
        match self.type:
          case 'geps':
            return "CMC_geps-raw_%s_%s_%s%s_P%s_allmbrs.grib2" % (variable, self.resolution, startDate, self.run_hour, formatedHour)
          case 'rdps':
            return "CMC_reg_%s_%s_%s%s_P%s.grib2" % (variable, self.resolution, startDate, self.run_hour, formatedHour)
          case 'hrdps':
            return "CMC_hrdps_%s_%s_%s_%s%s_P%s-00.grib2" % (self.domain, variable, self.resolution, startDate, self.run_hour, formatedHour)
          case 'default':
            return ''

    def getTypedURL(self, forecastHour = '000'):
      formatedHour = '%03d' % self.typeMultiplier(forecastHour)
      match self.type:
        case 'geps': return ("https://dd.weather.gc.ca/ensemble/geps/grib2/raw/%s/%s/" % (self.run_hour, formatedHour))
        case 'rdps': return ("https://dd.weather.gc.ca/model_gem_regional/%s/grib2/%s/%s/" % ((self.resolution).replace('ps', ''), self.run_hour, formatedHour))
        case 'hrdps': return ("https://dd.weather.gc.ca/model_hrdps/%s/grib2/%s/%s/" % (self.domain, self.run_hour, formatedHour))

    def formatURL(self, startDate, forecastHour, variable):
        urlBase = self.getTypedURL(forecastHour)
        return "%s%s" % (urlBase, self.formatFilename(startDate, forecastHour, variable))
        
    def getTimestampFromFilename(self, filename): 
        a = filename.split('_')
        date = a[len(a)-2]
        hour = a[len(a)-1][2:4]
        time = arrow.get(date, ('YYYYMMDD%s' % (self.runHour))).shift(hours=int(hour)).format()
        return time

    def generateFilenameList(self):
        if (not isinstance(self.variables, list)):
          raise RuntimeError("Variables is not an array.")
        names = []
        startDate = arrow.utcnow().to('-04:00').format('YYYYMMDD')
        for variable in self.variables:
            for hour in range(0, self.range_top):
                filename = self.formatFilename(startDate, hour, variable)
                names.append(filename)
        return names

    def typeMultiplier(self, value):
      casted_value = int(value)
      if self.type == 'geps':
        return casted_value * 3
      elif self.type == 'rdps':
        return casted_value * 1
      elif self.type == 'hrdps':
        return casted_value * 1
    
    def generateUrlList(self, variables=["TMP_TGL_2"]):
        if (not isinstance(variables, list)):
          raise RuntimeError("Variables is not an array.")
        names = []
        startDate = arrow.utcnow().to('-04:00').format('YYYYMMDD')
        for variable in variables:
            for hour in range(0, self.range_top):
                urlBase = self.getTypedURL(hour)
                filename = self.formatFilename(startDate, hour, variable)
                fullUrl = urlBase + filename
                names.append(fullUrl)
        return names

    @staticmethod
    def calculateRunStart(type):
        startDate = int(arrow.utcnow().format('HH'))
        if type == 'hrdps': 
          if startDate >= 0 and startDate < 6: return '18'
          if startDate >= 6 and startDate < 12: return '00'
          if startDate >= 12 and startDate < 18: return '06'
          if startDate >= 18 and startDate <= 24: return '12'
        
        return '00'
