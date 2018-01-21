import machine
import ubinascii

# These defaults are overwritten with the contents of /config.json by
# load_config()
CONFIG = {
    "broker": "192.168.1.19",
    "sensor_pin": 0,
    "led_pin": 2,
    "client_id": b"esp8266_" + ubinascii.hexlify(machine.unique_id()),
    "topic": b"home",
    "sleep_seconds": 60,
    "wireless_networks": {
        "wifi1": "passwork1",
        "wifi2": "password2"
    }
}


def load_config():
    import ujson as json
    try:
        with open("/config.json") as f:
            config = json.loads(f.read())
            return config
    except (OSError, ValueError):
        print("Couldn't load /config.json")
        save_config()
        return CONFIG


def save_config():
    import ujson as json
    try:
        with open("/config.json", "w") as f:
            f.write(json.dumps(CONFIG))
    except OSError:
        print("Couldn't save /config.json")
