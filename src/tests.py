import unittest
import arrow

from services.cmc import CMC
from services.file_manager import FileManager
from constants import geps_variables, rdps_variables

class TestCMC(unittest.TestCase):
    def test_formatFileName_geps_1(self):
        cmc = CMC('geps', resolution='latlon0p5x0p5', variables=geps_variables["temperature"], run_hour='12', range_top=48)
        filename = cmc.format_filename('20220101', '000', variable=geps_variables["temperature"][0])
        self.assertEqual(filename, 'CMC_geps-raw_TMP_TGL_2m_latlon0p5x0p5_2022010112_P000_allmbrs.grib2', "Is correct value")

    def test_formatFileName_geps_2(self):
        cmc = CMC('geps', resolution='latlon0p5x0p5', variables=geps_variables["temperature"], run_hour='00', range_top=48)
        filename = cmc.format_filename('20220102', '000', variable=geps_variables["temperature"][0])
        self.assertEqual(filename, 'CMC_geps-raw_TMP_TGL_2m_latlon0p5x0p5_2022010200_P000_allmbrs.grib2', "Is correct value")

    def test_formatFileName_hrdps_1(self):
        cmc = CMC('hrdps', resolution='ps2.5km', variables=rdps_variables["temperature"], run_hour='12', range_top=48, domain='west')
        filename = cmc.format_filename('20220101', '001', variable=rdps_variables["temperature"][0])
        self.assertEqual(filename, 'CMC_hrdps_west_TMP_TGL_2_ps2.5km_2022010112_P001-00.grib2', "Is correct value")

    def test_formatFileName_rdps_1(self):
        cmc = CMC('rdps', resolution='ps10km', variables=rdps_variables["temperature"], run_hour='00', range_top=48)
        filename = cmc.format_filename('20220418', '000', variable=rdps_variables["temperature"][0])
        self.assertEqual(filename, 'CMC_reg_TMP_TGL_2_ps10km_2022041800_P000.grib2', "Is correct value")

    def test_formatUrl_geps_1(self):
        cmc = CMC('geps', resolution='latlon0p5x0p5', variables=geps_variables["temperature"], run_hour='12', range_top=48)
        filename = cmc.format_url('20220101', '000', geps_variables["temperature"][0])
        self.assertEqual(filename, 'https://dd.weather.gc.ca/ensemble/geps/grib2/raw/12/000/CMC_geps-raw_TMP_TGL_2m_latlon0p5x0p5_2022010112_P000_allmbrs.grib2', "Is correct value")

    def test_formatUrl_rdps_1(self):
        cmc = CMC('rdps', resolution='ps10km', variables=rdps_variables["temperature"], run_hour='12', range_top=48)
        filename = cmc.format_url('20220418', '000', rdps_variables["temperature"][0])
        self.assertEqual(filename, 'https://dd.weather.gc.ca/model_gem_regional/10km/grib2/12/000/CMC_reg_TMP_TGL_2_ps10km_2022041812_P000.grib2', "Is correct value")

    def test_formatUrl_hrdps_1(self):
        cmc = CMC('hrdps', resolution='ps2.5km', variables=rdps_variables["temperature"], run_hour='12', range_top=48, domain="west")
        filename = cmc.format_url('20220418', '000', rdps_variables["temperature"][0])
        self.assertEqual(filename, 'https://dd.weather.gc.ca/model_hrdps/west/grib2/12/000/CMC_hrdps_west_TMP_TGL_2_ps2.5km_2022041812_P000-00.grib2', "Is correct value")

    def test_generate_url_list_geps(self):
        cmc = CMC('geps', resolution='latlon0p5x0p5', variables=geps_variables["temperature"], run_hour='12', range_top=5)
        filename = cmc.generate_url_list()
        currentDate = arrow.utcnow().to('-04:00').format('YYYYMMDD')
        results = [
            ('https://dd.weather.gc.ca/ensemble/geps/grib2/raw/12/000/CMC_geps-raw_TMP_TGL_2m_latlon0p5x0p5_%s12_P000_allmbrs.grib2' % (currentDate)),
            ('https://dd.weather.gc.ca/ensemble/geps/grib2/raw/12/003/CMC_geps-raw_TMP_TGL_2m_latlon0p5x0p5_%s12_P003_allmbrs.grib2' % (currentDate)),
            ('https://dd.weather.gc.ca/ensemble/geps/grib2/raw/12/006/CMC_geps-raw_TMP_TGL_2m_latlon0p5x0p5_%s12_P006_allmbrs.grib2' % (currentDate)),
            ('https://dd.weather.gc.ca/ensemble/geps/grib2/raw/12/009/CMC_geps-raw_TMP_TGL_2m_latlon0p5x0p5_%s12_P009_allmbrs.grib2' % (currentDate)),
            ('https://dd.weather.gc.ca/ensemble/geps/grib2/raw/12/012/CMC_geps-raw_TMP_TGL_2m_latlon0p5x0p5_%s12_P012_allmbrs.grib2' % (currentDate)),
        ]
        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(filename, results, "Is correct value")

    def test_generate_url_list_rdps(self):
        cmc = CMC('rdps', resolution='ps10km', variables=rdps_variables["temperature"], run_hour='12', range_top=5)
        filename = cmc.generate_url_list()
        currentDate = arrow.utcnow().to('-04:00').format('YYYYMMDD')
        results = [
            ('https://dd.weather.gc.ca/model_gem_regional/10km/grib2/12/000/CMC_reg_TMP_TGL_2_ps10km_%s12_P000.grib2' % (currentDate)),
            ('https://dd.weather.gc.ca/model_gem_regional/10km/grib2/12/001/CMC_reg_TMP_TGL_2_ps10km_%s12_P001.grib2' % (currentDate)),
            ('https://dd.weather.gc.ca/model_gem_regional/10km/grib2/12/002/CMC_reg_TMP_TGL_2_ps10km_%s12_P002.grib2' % (currentDate)),
            ('https://dd.weather.gc.ca/model_gem_regional/10km/grib2/12/003/CMC_reg_TMP_TGL_2_ps10km_%s12_P003.grib2' % (currentDate)),
            ('https://dd.weather.gc.ca/model_gem_regional/10km/grib2/12/004/CMC_reg_TMP_TGL_2_ps10km_%s12_P004.grib2' % (currentDate))
        ]
        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(filename, results, "Is correct value")

    def test_generate_url_list_hrdps(self):
        cmc = CMC('hrdps', resolution='ps2.5km', variables=rdps_variables["temperature"], run_hour='12', range_top=5)
        filename = cmc.generate_url_list()
        currentDate = arrow.utcnow().to('-04:00').format('YYYYMMDD')
        results = [
            ('https://dd.weather.gc.ca/model_hrdps/east/grib2/12/000/CMC_hrdps_east_TMP_TGL_2_ps2.5km_%s12_P000-00.grib2' % (currentDate)),
            ('https://dd.weather.gc.ca/model_hrdps/east/grib2/12/001/CMC_hrdps_east_TMP_TGL_2_ps2.5km_%s12_P001-00.grib2' % (currentDate)),
            ('https://dd.weather.gc.ca/model_hrdps/east/grib2/12/002/CMC_hrdps_east_TMP_TGL_2_ps2.5km_%s12_P002-00.grib2' % (currentDate)),
            ('https://dd.weather.gc.ca/model_hrdps/east/grib2/12/003/CMC_hrdps_east_TMP_TGL_2_ps2.5km_%s12_P003-00.grib2' % (currentDate)),
            ('https://dd.weather.gc.ca/model_hrdps/east/grib2/12/004/CMC_hrdps_east_TMP_TGL_2_ps2.5km_%s12_P004-00.grib2' % (currentDate)),
        ]
        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(filename, results, "Is correct value")

    def test_get_timestamp_from_filename(self):
      ts = FileManager.get_timestamp_from_filename('hrdps', 'CMC_hrdps_east_DEPR_ISBL_0175_ps2.5km_2011092412_P003-00.grib2')
      ## run_hour = 12
      ## P003 -> 12 + 03 = 15
      self.assertEqual("2011-09-24 15:00:00+00:00", ts, "Is correct value")

    def test_get_timestamp_from_filename_2(self):
      ts = FileManager.get_timestamp_from_filename('hrdps', 'CMC_hrdps_east_TMP_ISBL_0175_ps2.5km_2011092406_P021-00.grib2')
      self.assertEqual("2011-09-25 03:00:00+00:00", ts, "Is correct value")


if __name__ == '__main__':
    unittest.main()