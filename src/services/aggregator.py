from msilib.schema import File
import arrow
from services.file_manager import FileManager

## store dates as utc
## don't keep history
## use one file as db for now
aggregator_type = 'aggregated'

class Aggregator:
  def __init__(self, latitude, longitude):
    self.selected_filename = f'{aggregator_type}_{latitude}_{longitude}.json'
    self.in_data = { 'hrdps': {} }
    self.aggregated_data = {
      'current': {},
      'hourly': {},
      'last_aggregation_time': ''
    }

  def select_filename(self, filename):
    self.selected_filename = filename

  def save(self):
    return FileManager.save_json(aggregator_type, self.select_filename, self.aggregated_data)
      

  def load(self):
    if (FileManager.json_file_exists(aggregator_type, self.select_filename)):
      aggregator_file_contents = FileManager.open_json_file(aggregator_type)
      if (aggregator_file_contents['last_aggregation_time'] != ''):
        self.aggregated_data = aggregator_file_contents
    
