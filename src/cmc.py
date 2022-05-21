from ast import For
import arrow
import requests
import pygrib

from sty import fg
from os.path import exists
from constants import hrdps_path, geps_path
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

    def fetch_files(self, urls, files):
        needToFetch = False
        basepath = ""
        if self.type == 'hrdps':
          basepath = hrdps_path
        if self.type == 'geps':
          basepath = geps_path

        for file in files:
          if not FileManager.file_exists(basepath + file):
            needToFetch = True
        
        if not needToFetch:
          return ''

        FileManager.delete_all_files()
        FileManager.create_missing_files()

        for url in urls:
            r = requests.get(url=url)
            status = r.status_code
            if (status == 200):
              match self.type:
                case 'hrdps':
                  FileManager.add_hrdps_file("CMC_hrdps" + url.split("CMC_hrdps")[1], r.content)
                case 'geps':
                  FileManager.add_geps_file("CMC_geps-raw" + url.split("CMC_geps-raw")[1], r.content)
                case 'default':
                  cprint(fg.red, 'Not implemented')
            else:
              cprint(fg.red, "Recevied status code " + str(status) + " while fetching HRDPS GRIB2 file.")

    def load_grib_from_files(self, lat, lon, filePaths = []):
      match self.type:
        case 'hrdps':
          diff = 0.02
          data = []
          for filename in filePaths:
              file_path = hrdps_path + filename
              if (exists(file_path)): 
                  grbs = pygrib.open(hrdps_path + filename)
                  timestamp = FileManager.get_timestamp_from_filename(filename, 'hrdps')
                  grib_analyst = GribAnalyst(grbs)
                  inv1 = grib_analyst.get_inventory()
                  inv = str(inv1[0])
                  if (len(inv) > 0):
                      attr = inv.split(':')[1]
                      local_data = grib_analyst.find_central_data(attr, lat-diff, lat+diff, lon-diff, lon+diff)
                      local_data['time'] = timestamp
                      local_data['time'] = arrow.get(local_data['time']).to('America/New_York').shift(hours=int(self.run_hour)).format()
                      if (local_data['type'] == '2 metre temperature'):
                        local_data['value'] = round(local_data['value'] - 273.15, 2)
                      if (local_data['type'] == '2 metre specific humidity'):
                        local_data['value'] = round(local_data['value'] * 10000, 2)
                      if (local_data['type'] == 'Cloud water'):
                        local_data['value'] = round(local_data['value'], 2)
                      if (local_data['type'] == '10 metre wind speed'):
                        local_data['value'] = round(local_data['value'] * 3.6, 2)
                      data.append(local_data)
              else:
                cprint(fg.red, "No file to load.")

          return data

        case 'geps':
          diff = 0.5 
          data = []
          for filename in filePaths:
              file_path = geps_path + filename
              if (exists(file_path)): 
                  grbs = pygrib.open(file_path)
                  timestamp = FileManager.get_timestamp_from_filename(filename, 'geps')
                  grib_analyst = GribAnalyst(grbs)
                  inv1 = grib_analyst.get_inventory()
                  cprint(fg.cyan, "GEPS Inventory: ")
                  for i in inv1:
                    cprint(fg.yellow, str(i))
                  inv = str(inv1[0])
                  grib_analyst.get_info()
                  if (len(inv) > 0):
                      attr = inv.split(':')[1]
                      local_data = grib_analyst.find_central_data(attr, round(lat-diff, 1), round(lat+diff, 1), round(lon-diff+180, 1), round(lon+diff+180,1))
                      local_data['time'] = timestamp
                      local_data['time'] = arrow.get(local_data['time']).to('America/New_York').shift(hours=int(self.run_hour)).format()
                      cprint(fg.yellow, str(local_data))
                      #if (local_data['type'] == '2 metre temperature'):
                      #  local_data['value'] = round(local_data['value'] - 273.15, 2)
                      data.append(local_data)
              else:
                cprint(fg.red, "No file to load.")

          return []
        case 'default':
          cprint(fg.red, 'Not implemented')
          return []
      cprint(fg.yellow, self.type)

    def format_filename(self, start_date, forecast_hour, variable):
        formated_hour = '%03d' % self.type_multiplier(forecast_hour)
        match self.type:
          case 'geps':
            return "CMC_geps-raw_%s_%s_%s%s_P%s_allmbrs.grib2" % (variable, self.resolution, start_date, self.run_hour, formated_hour)
          case 'rdps':
            return "CMC_reg_%s_%s_%s%s_P%s.grib2" % (variable, self.resolution, start_date, self.run_hour, formated_hour)
          case 'hrdps':
            return "CMC_hrdps_%s_%s_%s_%s%s_P%s-00.grib2" % (self.domain, variable, self.resolution, start_date, self.run_hour, formated_hour)
          case 'default':
            return ''

    def get_typed_url(self, forecast_hour = '000'):
      formated_hour = '%03d' % self.type_multiplier(forecast_hour)
      match self.type:
        case 'geps': return ("https://dd.weather.gc.ca/ensemble/geps/grib2/raw/%s/%s/" % (self.run_hour, formated_hour))
        case 'rdps': return ("https://dd.weather.gc.ca/model_gem_regional/%s/grib2/%s/%s/" % ((self.resolution).replace('ps', ''), self.run_hour, formated_hour))
        case 'hrdps': return ("https://dd.weather.gc.ca/model_hrdps/%s/grib2/%s/%s/" % (self.domain, self.run_hour, formated_hour))

    def format_url(self, start_date, forecast_hour, variable):
        urlBase = self.get_typed_url(forecast_hour)
        return "%s%s" % (urlBase, self.format_filename(start_date, forecast_hour, variable))
        
    def get_timestamp_from_filename(self, filename): 
        a = filename.split('_')
        date = a[len(a)-2]
        hour = a[len(a)-1][2:4]
        time = arrow.get(date, ('YYYYMMDD%s' % (self.run_hour))).shift(hours=int(hour)).format()
        return time

    def generate_filename_list(self):
        if (not isinstance(self.variables, list)):
          raise RuntimeError("Variables is not an array.")
        names = []
        start_date = arrow.utcnow().to('America/New_York').format('YYYYMMDD')
        for variable in self.variables:
            for hour in range(0, self.range_top):
                filename = self.format_filename(start_date, hour, variable)
                names.append(filename)
        return names

    def type_multiplier(self, value):
      casted_value = int(value)
      if self.type == 'geps':
        return casted_value * 3
      elif self.type == 'rdps':
        return casted_value * 1
      elif self.type == 'hrdps':
        return casted_value * 1
    
    def generate_url_list(self, variables=["TMP_TGL_2"]):
        if (not isinstance(self.variables, list)):
          raise RuntimeError("Variables is not an array.")
        names = []
        start_date = arrow.utcnow().to('America/New_York').format('YYYYMMDD')
        for variable in self.variables:
            for hour in range(0, self.range_top):
                urlBase = self.get_typed_url(hour)
                filename = self.format_filename(start_date, hour, variable)
                fullUrl = urlBase + filename
                names.append(fullUrl)
        return names

    @staticmethod
    def calculate_run_start(type):
        start_date = int(arrow.utcnow().format('HH'))
        if type == 'hrdps': 
          if start_date >= 0 and start_date < 6: return '18'
          if start_date >= 6 and start_date < 12: return '00'
          if start_date >= 12 and start_date < 18: return '06'
          if start_date >= 18 and start_date <= 24: return '12'
        
        return '00'
