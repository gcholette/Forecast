import os
import arrow
import shutil

from constants import data_path, hrdps_path

class FileManager:
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