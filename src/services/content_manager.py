
import arrow
from models.current_forecast import CurrentForecast
from services.file_manager import FileManager
from services.cmc import CMC
from constants import rdps_variables, active_variable_names

timezone = 'America/New_York'
lat = 45.536325
lon = -73.491374

class ContentManager:
  def current(self):
    data = {}
    for (i, _) in self.cmc_hrdps_hourly_load():
      data = i

    curr_forecast = CurrentForecast(data)
    
    return curr_forecast.get()
    

  def cmc_hrdps_hourly_load(self):
    cmc_type = 'hrdps'
    now = arrow.utcnow().to('-04:00').format('YYYYMMDD')
    hours = 48
    resolution = 'ps2.5km'
    domain = 'east'
    run_hour = CMC.calculate_run_start(cmc_type)
    out_data = {}

    chosen_vars = []
    for var_name in active_variable_names:
      chosen_vars.append((rdps_variables[var_name][0], var_name))

    for v, name in chosen_vars:
      local_cmc = CMC(cmc_type, domain, resolution, [v], run_hour, hours)
      json_filename = ('hrdps_local_%s_%s_%s_%s_%s' % (now, v, lat, lon, run_hour))

      if not FileManager.json_file_exists(cmc_type, json_filename):
        filenames = local_cmc.generate_filename_list()
        urls = local_cmc.generate_url_list()

        yield (out_data, f'Fetching {name} HRDPS files')
        local_cmc.fetch_files(urls, filenames)

        yield (out_data, f'Loading {name} HRDPS data')
        loaded_data = local_cmc.load_grib_from_files(lat, lon, filenames)

        FileManager.save_json('hrdps', json_filename, loaded_data)
        out_data[name] = loaded_data
      else:
        loaded_data = FileManager.open_json_file(cmc_type, json_filename)
        out_data[name] = loaded_data
      
      yield (out_data, 'Up to date')

