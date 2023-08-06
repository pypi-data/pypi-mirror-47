"""Constants for ATAG API."""

DOMAIN = 'atag'
ATAG_HANDLE = 'atag_data'
DATA_LISTENER = 'atag_listener'
REQUEST_INFO = 1 + 8 + 64  # report, control, and details
SIGNAL_UPDATE_ATAG = 'atag_update'
CONF_INTERFACE = 'interface'

STATE_HEAT = 'heat'
STATE_ECO = 'eco'
STATE_AUTO = 'auto'
STATE_MANUAL = 'manual'
STATE_EXTEND = 'extend'
STATE_OFF = 'off'

DEFAULT_TIMEOUT = 15
DEFAULT_PORT = 10000
DEFAULT_SCAN_INTERVAL = 120

HTTP_HEADER = {
    'Content-type': 'applicaton/x-www-form-urlencoded;charset=UTF-8',
    'Connection': 'Close',
    'User-Agent': 'Mozilla/5.0 (compatible; AtagOneAPI/x; http://atag.one/)'
}

ATTR_CURRENT_TEMPERATURE = 'current_temperature'
ATTR_MAX_TEMP = 'max_temp'
ATTR_MIN_TEMP = 'min_temp'
ATTR_OPERATION_LIST = 'operation_list'
ATTR_OPERATION_MODE = 'operation_mode'
ATTR_OPERATION_MODE_INT = 'ch_mode'
ATTR_TEMPERATURE_SET = 'shown_set_temp'
ATTR_TEMPERATURE = 'temperature'
ATTR_REPORT_TIME = 'report_time'
BOILER_STATUS = 'boiler_status'
BOILER_CONF = 'boiler_config'
UPDATE_MODE = 'update_mode'
UPDATE_TEMP = 'update_temp'
PAIR_PATH = 'pair'
UPDATE_PATH = 'update'
RETRIEVE_PATH = 'retrieve'
UPDATE_REPLY = 'update_reply'
RETRIEVE_REPLY = 'retrieve_reply'
PAIR_REPLY = 'pair_reply'
STATUS = 'status'
REPORT = 'report'
CONTROL = 'control'
DETAILS = 'details'
ACC_STATUS = 'acc_status'
WEATHER_STATUS = 'weather_status'

DEFAULT_NAME = 'Atag One Thermostat'
DEFAULT_MIN_TEMP = 12
DEFAULT_MAX_TEMP = 21

SENSOR_PREFIX = 'Atag '
REPORT_STRUCTURE = {
    STATUS: ["device_id", "device_status", "connection_status", "date_time"],
    REPORT: ["report_time", "burning_hours", "device_errors", "boiler_errors", "room_temp",
             "outside_temp", "dbg_outside_temp", "pcb_temp", "ch_setpoint", "dhw_water_temp",
             "ch_water_temp", "dhw_water_pres", "ch_water_pres", "ch_return_temp",
             "boiler_status", "boiler_config", "ch_time_to_temp", "shown_set_temp",
             "power_cons", "tout_avg", "rssi", "current", "voltage", "charge_status",
             "lmuc_burner_starts", "dhw_flow_rate", "resets", "memory_allocation"],
    DETAILS: ["boiler_temp", "boiler_return_temp", "min_mod_level", "rel_mod_level",
              "boiler_capacity", "target_temp", "overshoot", "max_boiler_temp", "alpha_used",
              "regulation_state", "ch_m_dot_c", "c_house", "r_rad", "r_env", "alpha", "alpha_max",
              "delay", "mu", "threshold_offs", "wd_k_factor ", "wd_exponent",
              "lmuc_burner_hours", "lmuc_dhw_hours", "KP", "KI"],
    CONTROL: ["ch_status", "ch_control_mode", "ch_mode", "ch_mode_duration", "ch_mode_temp",
              "dhw_temp_setp", "dhw_status", "dhw_mode", "dhw_mode_temp", "weather_temp",
              "weather_status", "vacation_duration", "extend_duration", "fireplace_duration"]
}
SENSOR_TYPES = {
    'device_id': ['One ID', '', 'mdi:account-card-details-outline', 'device_id'],
    'device_status': ['One status', '', 'mdi:account-card-details-outline', 'device_status'],
    'connection_status': ['Connection', '', 'mdi:wifi', 'connection_status'],
    'date_time': ['Datetime', '', 'mdi:calendar-clock', 'date_time'],
    ATTR_CURRENT_TEMPERATURE: ['Current Temperature', '°C', 'mdi:thermometer', 'room_temp'],
    'outside_temp': ['Outside Temp', '°C', 'mdi:thermometer', 'outside_temp'],
    'outside_temp_avg': ['Average Outside Temperature', '°C', 'mdi:thermometer', 'tout_avg'],
    WEATHER_STATUS: ['Weather Status', '', 'mdi:white-balance-sunny', 'weather_status'],
    'pcb_temp': ['PCB Temperature', '°C', 'mdi:thermometer', 'pcb_temp'],
    ATTR_TEMPERATURE: ['Target Temperature', '°C', 'mdi:thermometer', ATTR_TEMPERATURE_SET],
    ATTR_OPERATION_MODE: ['Operation Mode', '', 'mdi:settings', ATTR_OPERATION_MODE_INT],
    'ch_water_pressure': ['Central Heating Pressure', 'Bar', 'mdi:gauge', 'ch_water_pres'],
    'ch_water_temp': ['CH Water Temperature', '°C', 'mdi:thermometer', 'ch_water_temp'],
    'ch_return_temp': ['CH Return Temperature', '°C', 'mdi:thermometer', 'ch_return_temp'],
    'dhw_water_temp': ['Hot Water Temp', '°C', 'mdi:thermometer', 'dhw_water_temp'],
    'dhw_water_pres': ['Hot Water Pressure', 'Bar', 'mdi:gauge', 'dhw_water_pres'],
    BOILER_STATUS: ['Boiler Status', '', 'mdi:flash', 'boiler_status'],
    BOILER_CONF: ['Boiler Config', '', 'mdi:flash', 'boiler_config'],
    'burning_hours': ['Burning Hours', 'h', 'mdi:fire', 'burning_hours'],
    'voltage': ['Voltage', 'V', 'mdi:flash', 'voltage'],
    'current': ['Current', 'mA', 'mdi:flash-auto', 'current'],
    'flame_level': ['Flame', '%', 'mdi:fire', 'rel_mod_level'],
    ATTR_REPORT_TIME: ['Report Time', '', 'mdi:clock', ATTR_REPORT_TIME],
    "ch_status": ["ch_status", '', 'mdi:flash', "ch_status"],
    "ch_control_mode": ["ch_control_mode", '', 'mdi:flash', "ch_control_mode"],
    "ch_mode_duration": ["ch_mode_duration", '', 'mdi:flash', "ch_mode_duration"],
    "dhw_temp_setp": ["dhw_temp_setpoint", '', 'mdi:flash', "dhw_temp_setp"],
    "dhw_status": ["dhw_status", '', 'mdi:flash', "dhw_status"],
    "dhw_mode": ["dhw_mode", '', 'mdi:flash', "dhw_mode"],
    "dhw_mode_temp": ["dhw_mode_temp", '', 'mdi:flash', "dhw_mode_temp"],
    "weather_temp": ["weather_temp", '', 'mdi:flash', "weather_temp"],
    "weather_status": ["weather_status", '', 'mdi:flash', "weather_status"],
    "vacation_duration": ["vacation_duration", '', 'mdi:flash', "vacation_duration"],
    "extend_duration": ["extend_duration", '', 'mdi:flash', "extend_duration"],
    "fireplace_duration": ["fireplace_duration", '', 'mdi:flash', "fireplace_duration"]
}

REPORT_STRUCTURE_INV = {
    v: i for i in REPORT_STRUCTURE for v in REPORT_STRUCTURE[i]}
BOILER_STATES = {
    14: 'Heating CV & Water',
    12: 'Heating Water',
    10: 'Heating CV',
    8: 'Heating Boiler',
    4: 'Water active',
    2: 'CV active',
    0: 'Idle'
}

CONNECTION_STATES = {
    23: "Connected to BCU"
}

CH_CONTROL_MODES = {
    0: 'Thermostat',
    1: 'Weather dependent'
}

# CH_STATUS = {
#     33: 'Heating type: Convectors / Air heating?', # 8
#     1: 'Heating type: Radiators & Floor'
# }

WEATHER_STATES = {
    0: ['Sunny', 'mdi:weather-sunny'],
    1: ['Clear', 'mdi:weather-night'],
    2: ['Rainy', 'mdi:weather-rainy'],
    3: ['Snowy', 'mdi:weather-snowy'],  # Not sure, Atag icons unclear
    4: ['Haily', 'mdi:weather-hail'],  # Not sure, Atag icons unclear
    5: ['Windy', 'mdi:weather-windy'],
    6: ['Misty', 'mdi:weather-fog'],
    7: ['Cloudy', 'mdi:weather-cloudy'],
    8: ['Partly Sunny', 'mdi:weather-partlycloudy'],
    9: ['Partly Cloudy', 'mdi:cloud'],  # Night with clouds..
    10: ['Shower', 'mdi:weather-pouring'],  # Not sure, Atag icons unclear
    11: ['Lightning', 'mdi:weather-lightning'],
    12: ['Hurricane', 'mdi:weather-hurricane'],
    13: ['Unknown', 'mdi:cloud-question']
}

# fix for Google Assistant integration - use HEAT instead of MANUAL
#MODES = {STATE_HEAT: 1, STATE_AUTO: 2, STATE_HOLD: 4}
MODES = {STATE_MANUAL: 1, STATE_AUTO: 2, STATE_EXTEND: 4}
INT_MODES = {v: k for k, v in MODES.items()}

CH_CONTROLS = {'Thermostat': 0, 'Weather based': 1}
INT_CH_CONTROLS = {v: k for k, v in CH_CONTROLS.items()}
