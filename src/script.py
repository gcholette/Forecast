import json
import time
import arrow
from file_manager import FileManager
from sty import fg
from cmc import CMC
from constants import *
from util import cprint, reorderData
from uniplot import plot
from yaspin import yaspin

timezone = 'America/New_York'
lat = 45.536325
lon = -73.491374

def extractValue(x):
  return (float(x['value']))

def extractTimestamp(x):
  return (arrow.get(x['time']).timestamp())

def yellow(txt):
  cprint(fg.yellow, txt)

def cyan(txt):
  cprint(fg.cyan, txt)

print('')
yellow('      :::::::::: ::::::::  :::::::::  :::::::::: ::::::::      :::      :::::::: ::::::::::: ')
yellow('     :+:       :+:    :+: :+:    :+: :+:       :+:    :+:   :+: :+:   :+:    :+:    :+:      ')
yellow('    +:+       +:+    +:+ +:+    +:+ +:+       +:+         +:+   +:+  +:+           +:+      ') 
yellow('   :#::+::#  +#+    +:+ +#++:++#:  +#++:++#  +#+        +#++:++#++: +#++:++#++    +#+       ') 
yellow('  +#+       +#+    +#+ +#+    +#+ +#+       +#+        +#+     +#+        +#+    +#+         ')
yellow(' #+#       #+#    #+# #+#    #+# #+#       #+#    #+# #+#     #+# #+#    #+#    #+#          ')
yellow('###        ########  ###    ### ########## ########  ###     ###  ########     ###         ') 
yellow('')


def getHRDPS(lat, lon, variables):
    cmc_type = 'hrdps'
    hours = 48
    resolution = 'ps2.5km'
    domain = 'east'
    now = arrow.utcnow().to('-04:00').format('YYYYMMDD')
    run_hour = CMC.calculateRunStart(cmc_type)
    json_filename = ('hrdps_local_%s_%s_%s_%s_%s' % (now, variables[0],lat,lon, run_hour))
    hrdps_cmc = CMC(cmc_type, domain, resolution, variables, run_hour, hours)
    data = []

    cprint(fg.da_grey, variables[0] + ' HRDPS Run Hour: ' + run_hour)

    if (not FileManager.jsonFileExists(cmc_type, json_filename)):
      filenames = hrdps_cmc.generateFilenameList()
      urls = hrdps_cmc.generateUrlList()
      with yaspin(text=(fg.cyan + "Fetching " + variables[0] + " HRDPS CMC GRIB2 Files..." + fg.rs), color="magenta") as sp:
          hrdps_cmc.fetchFiles(urls, filenames)
          sp.ok("✅")

      with yaspin(text=(fg.cyan + "Loading " + variables[0] + " data from GRIB2 Files..." + fg.rs), color="magenta") as sp:
          data = hrdps_cmc.loadGribFromFiles(lat, lon, filenames)
          sp.ok("✅")
      FileManager.saveJson('hrdps', json_filename, data)
    else:
      data = FileManager.openJsonFile(cmc_type, json_filename)

    return data

def getGEPS(lat, lon):
    cmc_type = 'geps'
    hours = 8
    variables = geps_variables['temperature']
    resolution = 'latlon0p5x0p5'
    domain = 'east'
    now = arrow.utcnow().to('-04:00').format('YYYYMMDD')
    run_hour = CMC.calculateRunStart(cmc_type)
    json_filename = ('geps_local_%s_%s_%s_%s' % (now, lat,lon, run_hour))
    cmc = CMC(cmc_type, domain, resolution, variables, run_hour, hours)
    data = []

    cprint(fg.cyan, 'Run Hour: ' + run_hour)
    cprint(fg.magenta, arrow.utcnow().to('-04:00').format('MM-DD HH:mm:ss'))
    cprint(fg.magenta, ('%s %s temperature (%s, %s)') % (cmc_type, domain, str(lat), str(lon))) # cmc_type + '' + domain + ' temperature, (' + str(lat) + ' ' + str(lon) + ') ' + domain)


    filenames = cmc.generateFilenameList()
    urls = cmc.generateUrlList()
    print('URLS: ' + str(urls))
    print('Filenames: ' + str(filenames))
    cmc.fetchFiles(urls, filenames)
    data = cmc.loadGribFromFiles(lat, lon, filenames)
    FileManager.saveJson('geps', json_filename, data)

    #if (not FileManager.jsonFileExists(cmc_type, json_filename)):
    #  filenames = cmc.generateFilenameList()
    #  urls = cmc.generateUrlList()
    #  print('URLS: ' + str(urls))
      #cmc.fetchFiles(urls, filenames)
      #data = cmc.loadGribFromFiles(lat, lon, filenames)
      #FileManager.saveJson('geps', json_filename, data)
    #else:
    #  data = FileManager.openJsonFile(cmc_type, json_filename)

    return data
 

def main():
    data1 = getHRDPS(lat, lon, rdps_variables['temperature'])
    data2 = getHRDPS(lat, lon, rdps_variables['humidity'])
    data3 = getHRDPS(lat, lon, rdps_variables['precipitation'])
    data5 = getHRDPS(lat, lon, rdps_variables['wind'])
    max_cols = 4
    hours_total = 48

    #data = getGEPS(lat, lon)

    def findValueInDataset(data, time):
      for x in data:
        if x['time'] == now_date:
          return x

    now_date = arrow.utcnow().to(timezone).format('YYYY-MM-DD HH:00:00ZZ')
    curr_elem1 = findValueInDataset(data1, time)
    curr_elem2 = findValueInDataset(data2, time)
    curr_elem3 = findValueInDataset(data3, time)
    curr_elem5 = findValueInDataset(data5, time)


    ys1 = list(map(extractValue, data1))
    xs1 = list(map(extractTimestamp, data1))

    ys2 = list(map(extractValue, data2))
    xs2 = list(map(extractTimestamp, data2))

    ys3 = list(map(extractValue, data3))
    xs3 = list(map(extractTimestamp, data3))

    ys5 = list(map(extractValue, data5))
    xs5 = list(map(extractTimestamp, data5))

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

    data1 = reorderData(data1, max_cols, hours_total)
    data2 = reorderData(data2, max_cols, hours_total)
    data3 = reorderData(data3, max_cols, hours_total)
    data5 = reorderData(data5, max_cols, hours_total)

    print(fg.da_grey + '\nSpecific Humidity' + fg.rs)
    print("Now: " + str(curr_elem2['value']) + " g/kg")
    plot(xs=[xs2],ys=[ys2], lines=True, color=True, y_gridlines=[0,25,50,75,100], x_gridlines=grids_x, width=84, height=12 )
    print("")
    for x, n in zip(data2, range(1, len(data2)+1)):
     print(fg.da_grey + '| ' + fg.yellow + arrow.get(x['time']).format('DD HH') + 'h ~ ' + fg.grey + str(x['value']).ljust(6) + ' g/kg' + fg.rs, end=" ")
     if n % max_cols == 0:
       print("")
    print("")

    print(fg.da_cyan + '\nCloud water density' + fg.rs)
    print("Now: " + str(curr_elem3['value']) + " kg/m2")
    plot(xs=[xs3, xs3, xs3],ys=[ys3, ys3, ys3], lines=True, color=True, y_gridlines=[0,10,20,30,40], x_gridlines=grids_x, width=84, height=12 )
    print("")
    for x, n in zip(data3, range(1, len(data2)+1)):
     print(fg.da_grey + '| ' + fg.yellow + arrow.get(x['time']).format('DD HH') + 'h ~ ' + fg.da_cyan + str(x['value']).ljust(6) + ' kg/m2' + fg.rs, end=" ")
     if n % max_cols == 0:
       print("")
    print("")

    print(fg.li_grey + '\nWind Speed' + fg.rs)
    print("Now: " + str(curr_elem5['value']) + " km/h")
    plot(xs=[xs5, xs5, xs5, xs5],ys=[ys5, ys5, ys5, ys5], lines=True, color=True, y_gridlines=[0,10,20,30,40], x_gridlines=grids_x, width=84, height=12 )
    print("")
    for x, n in zip(data5, range(1, len(data2)+1)):
     print(fg.da_grey + '| ' + fg.yellow + arrow.get(x['time']).format('DD HH') + 'h ~ ' + fg.da_cyan + str(x['value']).ljust(6) + ' km/h' + fg.rs, end=" ")
     if n % max_cols == 0:
       print("")
    print("")

    print(fg.li_red + '\nTemperature' + fg.rs)
    print("Now: " + str(curr_elem1['value']) + " °C")
    plot(xs=[xs1, xs1],ys=[ys1, ys1], lines=True, color=True, y_gridlines=[-10, -5,0,5,10,15,20,25,30,35, 40, 45], x_gridlines=grids_x, width=84, height=12 )
    print("")
    for x, n in zip(data1, range(1, len(data1)+1)):
      print(fg.da_grey + '| ' + fg.yellow + arrow.get(x['time']).format('DD HH') + 'h ~ ' + fg.li_red + str(x['value']).ljust(6) + ' °C' + fg.rs, end=" ")
      if n % max_cols == 0:
        print("")
    print("")

if __name__ == "__main__":
    main()
