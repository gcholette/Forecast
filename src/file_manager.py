import os
import json
import arrow
import shutil

from constants import data_path, hrdps_path, geps_path

class FileManager:
    @staticmethod
    def file_exists(fullpath):
      return os.path.exists(fullpath)

    @staticmethod
    def create_missing_files():
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        if not os.path.exists(data_path + 'cmc/'):
            os.mkdir(data_path + 'cmc/')
        if not os.path.exists(hrdps_path):
            os.mkdir(hrdps_path)
        if not os.path.exists(geps_path):
            os.mkdir(geps_path)

    @staticmethod
    def delete_all_files():
        if os.path.exists(data_path):
            shutil.rmtree(data_path + 'cmc/', True)
    
    @staticmethod
    def add_hrdps_file(filename, content): 
        path = data_path + 'cmc/hrdps/'
        with open(path + filename, 'wb') as f:
            f.write(content)

    @staticmethod
    def add_geps_file(filename, content): 
        path = data_path + 'cmc/geps/'
        with open(path + filename, 'wb') as f:
            f.write(content)

    @staticmethod
    def get_timestamp_from_filename(filename, cmc_type): 
        if cmc_type == 'hrdps':
          a = filename.split('_')
          date = a[len(a)-2]
          hour = a[len(a)-1][2:4]
          run_hour = date[8:10]
          time = arrow.get(date, 'YYYYMMDD' + run_hour).shift(hours=int(hour)).format()
          return time
        if cmc_type == 'geps':
          a = filename.split('_')
          date = a[6]
          hour = a[len(a)-2][2:4]
          run_hour = date[8:10]
          time = arrow.get(date, 'YYYYMMDD' + run_hour).shift(hours=int(hour)).format()
          return time

    
    @staticmethod
    def save_json(type, filename, content):
        path = data_path + 'json/' + type + '/' + filename

        if not os.path.exists(data_path + 'json/'):
            os.mkdir(data_path + 'json/')
        if not os.path.exists(data_path + 'json/' + type + '/'):
            os.mkdir(data_path + 'json/' + type + '/')

        with open(path, 'w') as f:
            f.write(json.dumps(content))


    @staticmethod
    def open_json_file(type, filename):
      path = data_path + 'json/' + type + '/' + filename
      j = open(path)
      return json.load(j)

    @staticmethod
    def json_file_exists(type, filename):
      path = data_path + 'json/' + type + '/' + filename
      return os.path.exists(path)


