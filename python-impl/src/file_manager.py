import os
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
