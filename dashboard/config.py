API_URL = "http://127.0.0.1:8000"

SETTING_DEFAULTS = {
    "setting_1": -0.0006,
    "setting_2": 0.0004,
    "setting_3": 100.0,
}

SENSOR_DEFAULTS = {
    "sensor_1": 518.67,
    "sensor_2": 642.58,
    "sensor_3": 1581.22,
    "sensor_4": 1398.91,
    "sensor_5": 14.62,
    "sensor_6": 21.61,
    "sensor_7": 554.42,
    "sensor_8": 2388.08,
    "sensor_9": 9056.4,
    "sensor_10": 1.3,
    "sensor_11": 47.23,
    "sensor_12": 521.79,
    "sensor_13": 2388.06,
    "sensor_14": 8130.11,
    "sensor_15": 8.4024,
    "sensor_16": 0.03,
    "sensor_17": 393.0,
    "sensor_18": 2388.0,
    "sensor_19": 100.0,
    "sensor_20": 38.81,
    "sensor_21": 23.3552,
}

FEATURE_COLUMNS = (
    list(SETTING_DEFAULTS.keys())
    + list(SENSOR_DEFAULTS.keys())
)

SENSOR_COLUMNS = list(SENSOR_DEFAULTS.keys())