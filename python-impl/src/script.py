from hrdps import HRDPSManager
from cmc import CMC
from constants import *
 
def main():
    print("Forecast service starting...")
    # hr = HRDPSManager(hours=48, variables=["TMP_TGL_2" ])
    # hr = HRDPSManager(hours=10, variables=["TMP_TGL_2"])
    # hr.loadGribFiles()
    # data = hr.loadData()
    # for x in data:
    #     print (str(x))
    cmc = CMC()

if __name__ == "__main__":
    main()