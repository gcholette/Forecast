import arrow

class CMC:
    # def loadGribFiles(self):
    #     print ("Requesting GRIB2 CMC HRDPS files...")
    #     lst = HRDPSFileListGenerator().generateUrlList(rangeTop=self.rangeTop, variables=self.variables)
    #     print("Url list:" + str(lst))
    #     FileManager.deleteAllFiles()
    #     FileManager.createMissingFiles()

    #     for url in lst:
    #         r = requests.get(url=url)
    #         status = r.status_code
    #         if (status == 200): 
    #           FileManager.addHRDPSFile("CMC_hrdps" + url.split("CMC_hrdps")[1], r.content)
    #         else:
    #           print("Recevied status code " + str(status) + " while fetching HRDPS GRIB2 file.")

    #     print ("Done.")

    #  CMC_hrdps_domain_Variable_LevelType_level_ps2.5km_YYYYMMDDHH_Phhh-mm.grib2
    #  Variable examples https://weather.gc.ca/grib/HRDPS_HR/HRDPS_nat_ps2p5km_P000_deterministic_e.html
    @staticmethod
    def formatFilename(type, startDate, runHour, forecastHour, variable, resolution, domain):
        match type:
          case 'geps':
            return "CMC_geps-raw_%s_%s_%s_%s%s_P%s_allmbrs.grib2" % (variable, resolution, startDate, runHour, forecastHour)
          case 'rdps':
            return "CMC_reg_%s_%s_%s_%s%s_P%s.grib2" % (variable, resolution, startDate, runHour, forecastHour)
          case 'hrdps':
            return "CMC_hrdps_%s_%s_%s_%s%s_P%s-00.grib2" % (domain, variable, resolution, startDate, runHour, forecastHour)
          case 'default':
            return ''

    @staticmethod
    def getTypedURL(type, startDate,  runHour = '12', forecastHour = '000', variable = 'TMP_TGL_2', resolution='ps2.5km', domain='east'):
      match type:
        case 'geps': return ("https://dd.weather.gc.ca/ensemble/geps/grib2/raw/%s/%s/" % (runHour, forecastHour))
        case 'rdps': return ("https://dd.weather.gc.ca/model_gem_regional/%s/grib2/%s/%s/" % (resolution, runHour, forecastHour))
        case 'hrdps': return ("https://dd.weather.gc.ca/model_hrdps/%s/grib2/%s/%s/" % (domain, runHour, forecastHour))

    @staticmethod
    def formatURL(type, startDate, runHour, forecastHour, variable, resolution, domain):
        urlBase = CMC.getTypedURL(type, startDate, runHour, forecastHour, variable, resolution, domain)
        return "%s%s/%s" % (urlBase, runHour, CMC.formatFilename(type, variable, resolution, startDate, runHour, domain))
        
    @staticmethod
    def getTimestampFromFilename(filename, runHour = 18): 
        a = filename.split('_')
        date = a[len(a)-2]
        hour = a[len(a)-1][2:4]
        time = arrow.get(date, ('YYYYMMDD%s' % (runHour))).shift(hours=int(hour)).format()
        return time

    @staticmethod
    def generateFilenameList(type, runHour = '12', forecastHour = '000', rangeTop=0, variables=["TMP_TGL_2"], resolution = 'ps2.5km', domain='east'):
        names = []
        startDate = arrow.utcnow().to('-04:00').format()
        for variable in variables:
            for hour in range(0, rangeTop):
                filename = CMC.formatFilename(type, startDate, runHour, forecastHour, variable, resolution, domain)
                names.append(filename)
        return names
    
    @staticmethod
    def generateUrlList(type, rangeTop=0, variables=["TMP_TGL_2"]):
        names = []
        urlBase = 'https://dd.weather.gc.ca/model_hrdps/east/grib2/18/'
        for variable in variables:
            for hour in range(0, rangeTop):
                hrdpsff = HRDPSFilenameFormatter(startDate=arrow.utcnow().to('-04:00').format(), hour=hour, variable=variable)
                filename = urlBase + ( '%03d/' % hour ) + CMC.formatFilename(type, startDate, runHour, forecastHour, variable, resolution, domain)
                names.append(filename)
        return names