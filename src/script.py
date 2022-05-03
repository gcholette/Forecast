import arrow
from cmc import CMC
from constants import *
 
def main():
    print("Forecast service starting...")

    cmc_type = 'hrdps'
    run_hour = '00'
    hours = 40
    variable = rdps_variables['temperature']
    resolution = 'ps2.5km'
    domain = 'east'

    filenames = CMC.generateFilenameList(cmc_type, run_hour, hours, variable, resolution, domain)
    urls = CMC.generateUrlList(cmc_type, run_hour, hours, variable, resolution, domain)

    CMC.fetchFiles(cmc_type, urls)
    data = CMC.loadGribFromFiles(cmc_type, run_hour, variable, filenames)

    for x in data:
      x['time'] = arrow.get(x['time']).to('-04:00').format()
      if (x['type'] == '2 metre temperature'):
        x['value'] = x['value'] - 273.15

      print (str(x))

if __name__ == "__main__":
    main()