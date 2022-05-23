version = "0.2.3"
timezone = 'America/New_York'
lat = 45.536325
lon = -73.491374

base_path = '/app/'
data_path = f'{base_path}data/'
hrdps_path = f'{data_path}cmc/hrdps/'
geps_path = f'{data_path}cmc/geps/'

active_variable_names = ['temperature', 'wind', 'humidity', 'precipitation']
spinner_frames_1 = ['_', '/','|', '\\']
spinner_frames_2 = ['_', '_','_', '_', '-','-','-','-']

TOO_SMALL_BOUNDARY_X = 68
SMALL_BOUNDARY_X = 75 
MEDIUM_BOUNDARY_X = 100 
LARGE_BOUNDARY_X = 150 
X_LARGE_BOUNDARY_X = 250 

geps_variables = {
  "temperature": ["TMP_TGL_2m"]
}

rdps_variables = {
  "temperature": ["TMP_TGL_2"],
  "humidity": ["SPFH_TGL_2"],
  "precipitation": ["CWAT_EATM_0"],
  "dew": ["DEPR_TGL_2"],
  "wind": ["WIND_TGL_10"]
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

splash_strs = [
  '      :::::::::: ::::::::  :::::::::  :::::::::: ::::::::      :::      :::::::: ::::::::::: ',
  '     :+:       :+:    :+: :+:    :+: :+:       :+:    :+:   :+: :+:   :+:    :+:    :+:      ',
  '    +:+       +:+    +:+ +:+    +:+ +:+       +:+         +:+   +:+  +:+           +:+      ', 
  '   :#::+::#  +#+    +:+ +#++:++#:  +#++:++#  +#+        +#++:++#++: +#++:++#++    +#+       ', 
  '  +#+       +#+    +#+ +#+    +#+ +#+       +#+        +#+     +#+        +#+    +#+         ',
  ' #+#       #+#    #+# #+#    #+# #+#       #+#    #+# #+#     #+# #+#    #+#    #+#          ',
  '###        ########  ###    ### ########## ########  ###     ###  ########     ###         ', 
  ''
]

short_splash_strs = [
' _____                         _   ',
'|   __|___ ___ ___ ___ ___ ___| |_ ',
'|   __| . |  _| -_|  _| .\'|_ -|  _|',
'|__|  |___|_| |___|___|__,|___|_|',
''
]