# Edited by Yunchi Lu on Mar.5th 2021 
'''
FREQUENCY: sampling rate [1 /s]
SA_ACC_THREASHOLD: acceleration activation threashold [m/s**2 *s]
SA_DURATION_THREASHOLD: continuous sharp acceleration period [s]
FT_SPEED_THREASHOLD: turn speed activation threashold [km/h *s]
FT_GYRO_THREASHOLD: turn angle activation threashold [rad/s *s]
FT_DURATION_THREASHOLD: continuous fast turn period [s]
FT_CD: cool down interval between two turns [s]
'''
defaultParameters = {
    'FREQUENCY': 50,
    'SA_ACC_THREASHOLD': 2,
    'SA_DURATION_THREASHOLD': 2,
    'FT_SPEED_THREASHOLD': 10,
    'FT_GYRO_THREASHOLD': 0.05,
    'FT_DURATION_THREASHOLD': 2,
    'FT_CD': 10
}
