import unittest
import arrow

from cmc import CMC
from constants import geps_variables, rdps_variables

class TestCMC(unittest.TestCase):
    def test_formatFileName_geps_1(self):
        filename = CMC.formatFilename('geps', '20220101', '12', '000', geps_variables["temperature"][0], 'latlon0p5x0p5')
        self.assertEqual(filename, 'CMC_geps-raw_TMP_TGL_2m_latlon0p5x0p5_2022010112_P000_allmbrs.grib2', "Is correct value")

    def test_formatFileName_geps_2(self):
        filename = CMC.formatFilename('geps', '20220102', '00', '000', geps_variables["temperature"][0], 'latlon0p5x0p5')
        self.assertEqual(filename, 'CMC_geps-raw_TMP_TGL_2m_latlon0p5x0p5_2022010200_P000_allmbrs.grib2', "Is correct value")

    def test_formatFileName_hrdps_1(self):
        filename = CMC.formatFilename('hrdps', '20220101', '12', '001', rdps_variables["temperature"][0], 'ps2.5km', 'west')
        self.assertEqual(filename, 'CMC_hrdps_west_TMP_TGL_2_ps2.5km_2022010112_P001-00.grib2', "Is correct value")

    def test_formatFileName_rdps_1(self):
        filename = CMC.formatFilename('rdps', '20220418', '00', '000', rdps_variables["temperature"][0], 'ps10km')
        self.assertEqual(filename, 'CMC_reg_TMP_TGL_2_ps10km_2022041800_P000.grib2', "Is correct value")

    def test_formatUrl_geps_1(self):
        filename = CMC.formatURL('geps', '20220101', '12', '000', geps_variables["temperature"][0], 'latlon0p5x0p5')
        self.assertEqual(filename, 'https://dd.weather.gc.ca/ensemble/geps/grib2/raw/12/000/CMC_geps-raw_TMP_TGL_2m_latlon0p5x0p5_2022010112_P000_allmbrs.grib2', "Is correct value")

    def test_formatUrl_rdps_1(self):
        filename = CMC.formatURL('rdps', '20220418', '12', '000', rdps_variables["temperature"][0], 'ps10km')
        self.assertEqual(filename, 'https://dd.weather.gc.ca/model_gem_regional/10km/grib2/12/000/CMC_reg_TMP_TGL_2_ps10km_2022041812_P000.grib2', "Is correct value")

    def test_formatUrl_hrdps_1(self):
        filename = CMC.formatURL('hrdps', '20220418', '12', '000', rdps_variables["temperature"][0], 'ps2.5km', 'west')
        self.assertEqual(filename, 'https://dd.weather.gc.ca/model_hrdps/west/grib2/12/000/CMC_hrdps_west_TMP_TGL_2_ps2.5km_2022041812_P000-00.grib2', "Is correct value")

    def test_generateUrlList_geps_1(self):
        filename = CMC.generateUrlList('geps', '12', 3, geps_variables["temperature"][0], 'latlon0p5x0p5')
        currentDate = arrow.utcnow().to('-04:00').format()
        results = [
            ('https://dd.weather.gc.ca/ensemble/geps/grib2/raw/12/000/CMC_geps-raw_TMP_TGL_2m_latlon0p5x0p5_%s12_P000_allmbrs.grib2' % (currentDate))
        ]
        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(filename, results, "Is correct value")

if __name__ == '__main__':
    unittest.main()