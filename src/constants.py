data_path = '/app/data/'
hrdps_path = '/app/data/cmc/hrdps/'
geps_path = '/app/data/cmc/geps/'

geps_variables = {
  "temperature": ["TMP_TGL_2m"]
}

rdps_variables = {
  "temperature": ["TMP_TGL_2"]
}

# En Kelvin
temperature_variables = ["TMP_TGL_2", "TMP_TGL_40", "TMP_ISBL_1015", "TMP_ISBL_1000"]

# humidité spécifique en kg kg-1
humidity_variables = ["SPFH_TGL_2", "SPFH_TGL_40", "SPFH_ISBL_1015", "SPFH_ISBL_0985"]

# precipitable water in kg m-2
precipitation_variables = ["PWAT_EATM_0", "CWAT_EATM_0"]

# wind speed in m/sec
wind_variables = ["WDIR_TGL_10", "WIND_TGL_10"]


## links
# https://dd.weather.gc.ca/model_gem_regional/10km/grib2/12/000/CMC_reg_TMP_TGL_2_ps10km_2022041712_P000.grib2