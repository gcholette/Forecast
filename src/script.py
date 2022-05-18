from curses.textpad import rectangle
import arrow
import sys
from file_manager import FileManager
from sty import fg
from cmc import CMC
from constants import *
from util import cprint, reorder_data, str_in_list
from uniplot import plot
from yaspin import yaspin
from curses import wrapper
from app import App

timezone = 'America/New_York'
lat = 45.536325
lon = -73.491374

def extract_value(x):
  return (float(x['value']))

def extract_timestamp(x):
  return (arrow.get(x['time']).timestamp())

def yellow(txt):
  cprint(fg.yellow, txt)

def cyan(txt):
  cprint(fg.cyan, txt)

def get_hrdps(lat, lon, variables):
    cmc_type = 'hrdps'
    hours = 48
    resolution = 'ps2.5km'
    domain = 'east'
    now = arrow.utcnow().to('-04:00').format('YYYYMMDD')
    run_hour = CMC.calculate_run_start(cmc_type)
    json_filename = ('hrdps_local_%s_%s_%s_%s_%s' % (now, variables[0],lat,lon, run_hour))
    hrdps_cmc = CMC(cmc_type, domain, resolution, variables, run_hour, hours)
    data = []

    cprint(fg.da_grey, variables[0] + ' HRDPS Run Hour: ' + run_hour)

    if (not FileManager.json_file_exists(cmc_type, json_filename)):
      filenames = hrdps_cmc.generate_filename_list()
      urls = hrdps_cmc.generate_url_list()
      with yaspin(text=(fg.cyan + "Fetching " + variables[0] + " HRDPS CMC GRIB2 Files..." + fg.rs), color="magenta") as sp:
          hrdps_cmc.fetch_files(urls, filenames)
          sp.ok("✅")

      with yaspin(text=(fg.cyan + "Loading " + variables[0] + " data from GRIB2 Files..." + fg.rs), color="magenta") as sp:
          data = hrdps_cmc.load_grib_from_files(lat, lon, filenames)
          sp.ok("✅")
      FileManager.save_json('hrdps', json_filename, data)
    else:
      data = FileManager.open_json_file(cmc_type, json_filename)

    return data

def get_geps(lat, lon):
    cmc_type = 'geps'
    hours = 8
    variables = geps_variables['temperature']
    resolution = 'latlon0p5x0p5'
    domain = 'east'
    now = arrow.utcnow().to('-04:00').format('YYYYMMDD')
    run_hour = CMC.calculate_run_start(cmc_type)
    json_filename = ('geps_local_%s_%s_%s_%s' % (now, lat,lon, run_hour))
    cmc = CMC(cmc_type, domain, resolution, variables, run_hour, hours)
    data = []

    cprint(fg.cyan, 'Run Hour: ' + run_hour)
    cprint(fg.magenta, arrow.utcnow().to('-04:00').format('MM-DD HH:mm:ss'))
    cprint(fg.magenta, ('%s %s temperature (%s, %s)') % (cmc_type, domain, str(lat), str(lon))) # cmc_type + '' + domain + ' temperature, (' + str(lat) + ' ' + str(lon) + ') ' + domain)


    filenames = cmc.generate_filename_list()
    urls = cmc.generate_url_list()
    print('URLS: ' + str(urls))
    print('Filenames: ' + str(filenames))
    cmc.fetch_files(urls, filenames)
    data = cmc.load_grib_from_files(lat, lon, filenames)
    FileManager.save_json('geps', json_filename, data)

    #if (not FileManager.json_file_exists(cmc_type, json_filename)):
    #  filenames = cmc.generate_filename_list()
    #  urls = cmc.generate_url_list()
    #  print('URLS: ' + str(urls))
      #cmc.fetch_files(urls, filenames)
      #data = cmc.load_grib_from_files(lat, lon, filenames)
      #FileManager.save_json('geps', json_filename, data)
    #else:
    #  data = FileManager.open_json_file(cmc_type, json_filename)

    return data
 

def run_prediction():
    print('')
    yellow('      :::::::::: ::::::::  :::::::::  :::::::::: ::::::::      :::      :::::::: ::::::::::: ')
    yellow('     :+:       :+:    :+: :+:    :+: :+:       :+:    :+:   :+: :+:   :+:    :+:    :+:      ')
    yellow('    +:+       +:+    +:+ +:+    +:+ +:+       +:+         +:+   +:+  +:+           +:+      ') 
    yellow('   :#::+::#  +#+    +:+ +#++:++#:  +#++:++#  +#+        +#++:++#++: +#++:++#++    +#+       ') 
    yellow('  +#+       +#+    +#+ +#+    +#+ +#+       +#+        +#+     +#+        +#+    +#+         ')
    yellow(' #+#       #+#    #+# #+#    #+# #+#       #+#    #+# #+#     #+# #+#    #+#    #+#          ')
    yellow('###        ########  ###    ### ########## ########  ###     ###  ########     ###         ') 
    yellow('')

    data1 = get_hrdps(lat, lon, rdps_variables['temperature'])
    data2 = get_hrdps(lat, lon, rdps_variables['humidity'])
    data3 = get_hrdps(lat, lon, rdps_variables['precipitation'])
    data5 = get_hrdps(lat, lon, rdps_variables['wind'])
    max_cols = 4
    hours_total = 48

    #data = getGEPS(lat, lon)

    def find_value_in_dataset(data, time):
      for x in data:
        if x['time'] == time:
          return x

    now_date = arrow.utcnow().to(timezone).format('YYYY-MM-DD HH:00:00ZZ')
    now_date1 = arrow.utcnow().to(timezone).shift(hours=+1).format('YYYY-MM-DD HH:00:00ZZ')
    now_date2 = arrow.utcnow().to(timezone).shift(hours=+2).format('YYYY-MM-DD HH:00:00ZZ')
    now_values = [
      find_value_in_dataset(data1, now_date),
      find_value_in_dataset(data2, now_date),
      find_value_in_dataset(data3, now_date),
      find_value_in_dataset(data5, now_date),
    ]

    now_values1 = [
      find_value_in_dataset(data1, now_date1),
      find_value_in_dataset(data2, now_date1),
      find_value_in_dataset(data3, now_date1),
      find_value_in_dataset(data5, now_date1),
    ]

    now_values2 = [
      find_value_in_dataset(data1, now_date2),
      find_value_in_dataset(data2, now_date2),
      find_value_in_dataset(data3, now_date2),
      find_value_in_dataset(data5, now_date2),
    ]

    
    ys1 = list(map(extract_value, data1))
    xs1 = list(map(extract_timestamp, data1))

    ys2 = list(map(extract_value, data2))
    xs2 = list(map(extract_timestamp, data2))

    ys3 = list(map(extract_value, data3))
    xs3 = list(map(extract_timestamp, data3))

    ys5 = list(map(extract_value, data5))
    xs5 = list(map(extract_timestamp, data5))

    grids_x = [
      arrow.utcnow().to(timezone).shift(minutes=-5).timestamp(),
      arrow.utcnow().to(timezone).shift(minutes=+5).timestamp(),
      arrow.utcnow().to(timezone).replace(hour=6, minute=0).timestamp(),
      arrow.utcnow().to(timezone).replace(hour=12, minute=0).timestamp(),
      arrow.utcnow().to(timezone).replace(hour=17, minute=0).timestamp(),
      arrow.utcnow().to(timezone).replace(hour=23, minute=59).timestamp(),
      arrow.utcnow().to(timezone).shift(days=+1).replace(hour=6, minute=0).timestamp(),
      arrow.utcnow().to(timezone).shift(days=+1).replace(hour=12, minute=0).timestamp(),
      arrow.utcnow().to(timezone).shift(days=+1).replace(hour=17, minute=0).timestamp(),
      arrow.utcnow().to(timezone).shift(days=+1).replace(hour=23, minute=59).timestamp()
    ]

    data1 = reorder_data(data1, max_cols, hours_total)
    data2 = reorder_data(data2, max_cols, hours_total)
    data3 = reorder_data(data3, max_cols, hours_total)
    data5 = reorder_data(data5, max_cols, hours_total)

    print(fg.da_grey + '\nSpecific Humidity' + fg.rs)
    plot(xs=[xs2],ys=[ys2], lines=True, color=True, y_gridlines=[0,25,50,75,100], x_gridlines=grids_x, width=84, height=12 )
    print("")
    for x, n in zip(data2, range(1, len(data2)+1)):
     print(fg.da_grey + '| ' + fg.yellow + arrow.get(x['time']).format('DD HH') + 'h ~ ' + fg.grey + str(x['value']).ljust(6) + ' g/kg' + fg.rs, end=" ")
     if n % max_cols == 0:
       print("")
    print("")

    print(fg.da_cyan + '\nCloud water density' + fg.rs)
    plot(xs=[xs3, xs3, xs3],ys=[ys3, ys3, ys3], lines=True, color=True, y_gridlines=[0,10,20,30,40], x_gridlines=grids_x, width=84, height=12 )
    print("")
    for x, n in zip(data3, range(1, len(data2)+1)):
     print(fg.da_grey + '| ' + fg.yellow + arrow.get(x['time']).format('DD HH') + 'h ~ ' + fg.da_cyan + str(x['value']).ljust(6) + ' kg/m2' + fg.rs, end=" ")
     if n % max_cols == 0:
       print("")
    print("")

    print(fg.li_grey + '\nWind Speed' + fg.rs)
    plot(xs=[xs5, xs5, xs5, xs5],ys=[ys5, ys5, ys5, ys5], lines=True, color=True, y_gridlines=[0,10,20,30,40], x_gridlines=grids_x, width=84, height=12 )
    print("")
    for x, n in zip(data5, range(1, len(data2)+1)):
     print(fg.da_grey + '| ' + fg.yellow + arrow.get(x['time']).format('DD HH') + 'h ~ ' + fg.da_cyan + str(x['value']).ljust(6) + ' km/h' + fg.rs, end=" ")
     if n % max_cols == 0:
       print("")
    print("")

    print(fg.li_red + '\nTemperature' + fg.rs)
    plot(xs=[xs1, xs1],ys=[ys1, ys1], lines=True, color=True, y_gridlines=[-10, -5,0,5,10,15,20,25,30,35, 40, 45], x_gridlines=grids_x, width=84, height=12 )
    print("")
    for x, n in zip(data1, range(1, len(data1)+1)):
      print(fg.da_grey + '| ' + fg.yellow + arrow.get(x['time']).format('DD HH') + 'h ~ ' + fg.li_red + str(x['value']).ljust(6) + ' °C' + fg.rs, end=" ")
      if n % max_cols == 0:
        print("")
    print("")

    print("             " + fg.li_red + "Temperature   " + fg.da_grey + "Humidity      " + fg.da_cyan + "Cloud water    " + fg.li_grey + "Wind speed")
    print(fg.cyan + "Current:     " + fg.li_red + str(now_values[0]['value']).ljust(6) + ' °C     ', end="")
    print(fg.da_grey + str(now_values[1]['value']).ljust(6) + ' g/kg   ', end="")
    print(fg.da_cyan + str(now_values[2]['value']).ljust(6) + ' kg/m2   ', end="")
    print(fg.li_grey + str(now_values[3]['value']).ljust(6) + ' km/h \n' + fg.rs, end="")

    print(fg.cyan + "Next hour:   " + fg.li_red + str(now_values1[0]['value']).ljust(6) + ' °C     ', end="")
    print(fg.da_grey + str(now_values1[1]['value']).ljust(6) + ' g/kg   ', end="")
    print(fg.da_cyan + str(now_values1[2]['value']).ljust(6) + ' kg/m2   ', end="")
    print(fg.li_grey + str(now_values1[3]['value']).ljust(6) + ' km/h \n' + fg.rs, end="")

    print(fg.cyan + "In 2 hours:  " + fg.li_red + str(now_values2[0]['value']).ljust(6) + ' °C     ', end="")
    print(fg.da_grey + str(now_values2[1]['value']).ljust(6) + ' g/kg   ', end="")
    print(fg.da_cyan + str(now_values2[2]['value']).ljust(6) + ' kg/m2   ', end="")
    print(fg.li_grey + str(now_values2[3]['value']).ljust(6) + ' km/h \n' + fg.rs, end="")


def fullscreen_app():
  app = App()
  wrapper(app.display)

def main():
  if str_in_list('--fullscreen', sys.argv):
    fullscreen_app()
  else:
    run_prediction()

if __name__ == "__main__":
  main()
