import json
import time
import arrow
from file_manager import FileManager
from sty import fg
from cmc import CMC
from constants import *
from util import cprint
from uniplot import plot
from yaspin import yaspin

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


def getHRDPS(lat, lon):
    cmc_type = 'hrdps'
    hours = 48
    variables = rdps_variables['temperature']
    resolution = 'ps2.5km'
    domain = 'east'
    now = arrow.utcnow().to('-04:00').format('YYYYMMDD')
    run_hour = CMC.calculateRunStart(cmc_type)
    json_filename = ('hrdps_local_%s_%s_%s_%s' % (now, lat,lon, run_hour))
    hrdps_cmc = CMC(cmc_type, domain, resolution, variables, run_hour, hours)
    data = []

    cprint(fg.cyan, 'Run Hour: ' + run_hour)
    cprint(fg.magenta, arrow.utcnow().to('-04:00').format('MM-DD HH:mm:ss'))

    if (not FileManager.jsonFileExists(cmc_type, json_filename)):
      filenames = hrdps_cmc.generateFilenameList()
      urls = hrdps_cmc.generateUrlList()
      with yaspin(text=(fg.cyan + "Fetching HRDPS CMC GRIB2 Files..." + fg.rs), color="magenta") as sp:
          hrdps_cmc.fetchFiles(urls, filenames)
          sp.ok("✅")

      with yaspin(text=(fg.cyan + "Loading data from GRIB2 Files..." + fg.rs), color="magenta") as sp:
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
    cprint(fg.cyan, "Forecast service starting...")

    lat = 45.536325
    lon = -73.491374

    data = getHRDPS(lat, lon)
    #data = getGEPS(lat, lon)

    ys = list(map(extractValue, data))
    xs = list(map(extractTimestamp, data))
    grids_x = [
      arrow.utcnow().to('-04:00').shift(minutes=-5).timestamp(),
      arrow.utcnow().to('-04:00').shift(minutes=+5).timestamp(),
      arrow.utcnow().to('-04:00').replace(hour=6, minute=0).timestamp(),
      arrow.utcnow().to('-04:00').replace(hour=12, minute=0).timestamp(),
      arrow.utcnow().to('-04:00').replace(hour=17, minute=0).timestamp(),
      arrow.utcnow().to('-04:00').replace(hour=23, minute=59).timestamp(),
      arrow.utcnow().to('-04:00').shift(days=+1).replace(hour=6, minute=0).timestamp(),
      arrow.utcnow().to('-04:00').shift(days=+1).replace(hour=12, minute=0).timestamp(),
      arrow.utcnow().to('-04:00').shift(days=+1).replace(hour=17, minute=0).timestamp(),
      arrow.utcnow().to('-04:00').shift(days=+1).replace(hour=23, minute=59).timestamp()
    ]

    plot(xs=[xs, xs],ys=[ys, ys], lines=True, color=True, y_gridlines=[-10, -5,0,5,10,15,20,25,30,35], x_gridlines=grids_x, width=84, height=12 )

    for x in data:
     print(fg.yellow + arrow.get(x['time']).format('MM-DD HH') + 'h | ' + fg.cyan + str(x['value']) + ' °C' + fg.rs)


if __name__ == "__main__":
    main()
