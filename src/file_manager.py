import os
import json
import arrow
import shutil

from constants import data_path, hrdps_path

class FileManager:
    @staticmethod
    def fileExists(file):
      path = data_path + 'cmc/hrdps/'
      return os.path.exists(path + file)

    @staticmethod
    def createMissingFiles():
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        if not os.path.exists(data_path + 'cmc/'):
            os.mkdir(data_path + 'cmc/')
        if not os.path.exists(hrdps_path):
            os.mkdir(hrdps_path)

    @staticmethod
    def deleteAllFiles():
        if os.path.exists(data_path):
            shutil.rmtree(data_path + 'cmc/', True)
    
    @staticmethod
    def addHRDPSFile(filename, content): 
        path = data_path + 'cmc/hrdps/'
        with open(path + filename, 'wb') as f:
            f.write(content)

    @staticmethod
    def getTimestampFromFilename(filename): 
        a = filename.split('_')
        date = a[len(a)-2]
        hour = a[len(a)-1][2:4]
        run_hour = date[8:10]
        time = arrow.get(date, 'YYYYMMDD' + run_hour).shift(hours=int(hour)).format()
        return time
    
    @staticmethod
    def saveJson(type, filename, content):
        path = data_path + 'json/' + type + '/' + filename

        if not os.path.exists(data_path + 'json/'):
            os.mkdir(data_path + 'json/')
        if not os.path.exists(data_path + 'json/' + type + '/'):
            os.mkdir(data_path + 'json/' + type + '/')

        with open(path, 'w') as f:
            f.write(json.dumps(content))


    @staticmethod
    def openJsonFile(type, filename):
      path = data_path + 'json/' + type + '/' + filename
      j = open(path)
      return json.load(j)

    @staticmethod
    def jsonFileExists(type, filename):
      path = data_path + 'json/' + type + '/' + filename
      return os.path.exists(path)


