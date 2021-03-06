import machine
import time
import dht

from umqtt.robust import MQTTClient

from config import load_config


def temperature_f(self):
    """Current tempurature in fahrenheit

    Adds a method to the DHT22 class which returns the tempurature in fahrenheit
    """
    return (self.temperature() * 1.8) + 32


def setup_pins():
    global DHT_PIN
    global LED_PIN

    dht.DHT22.temperature_f = temperature_f
    DHT_PIN = dht.DHT22(machine.Pin(CONFIG['sensor_pin']))
    LED_PIN = machine.Pin(CONFIG['led_pin'], machine.Pin.OUT)


def error_blink(duration=10):
    for count in range(duration):
        LED_PIN.on()
        time.sleep_ms(500)
        LED_PIN.off()
        time.sleep_ms(500)


def build_mqtt_topic(*args):
    """Join topic components with a '/' delimeters and encode as bytes

    The umqtt library expects topic to be byte encoded

    Arguments:
        *args {string} -- String to be added to topic

    Returns:
        [bytearray] -- byte encoded mqtt topic
    """
    topic = '/'.join(args)
    return topic.encode('utf-8')


def main():
    client = MQTTClient(CONFIG['client_id'], CONFIG['broker'])
    temperature_topic = build_mqtt_topic(CONFIG['topic'], CONFIG['client_id'], 'temperature')
    humidity_topic = build_mqtt_topic(CONFIG['topic'], CONFIG['client_id'], 'humidity')

    try:
        client.connect()
    except OSError:
        print("Failed to connect to broker {}, will retry...".format(CONFIG['broker']))
        error_blink(10)
        main()

    print("Connected to {}".format(CONFIG['broker']))
    while True:
        DHT_PIN.measure()
        client.publish(temperature_topic, b'{0:.0f}'.format(DHT_PIN.temperature_f()))
        client.publish(humidity_topic, b'{0:.0f}'.format(DHT_PIN.humidity()))

        print('Temperature: {0:.0f}, Humidity: {1:.0f}'.format(DHT_PIN.temperature_f(), DHT_PIN.humidity()))
        time.sleep(CONFIG['sleep_seconds'])


if __name__ == '__main__':
    CONFIG = load_config()
    setup_pins()
    main()
