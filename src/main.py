import machine
import time
import dht

from umqtt.robust import MQTTClient

from config import load_config


def temperature_f(self):
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


def main():
    client = MQTTClient(CONFIG['client_id'], CONFIG['broker'])

    try:
        client.connect()
    except OSError:
        print("Failed to connect to broker {}, will retry...".format(CONFIG['broker']))
        error_blink(10)
        main()

    print("Connected to {}".format(CONFIG['broker']))
    while True:
        DHT_PIN.measure()
        client.publish('{}/{}/temperature'.format(
            CONFIG['topic'], CONFIG['client_id']), bytes(str(DHT_PIN.temperature_f()), 'utf-8'))

        client.publish('{}/{}/humidity'.format(
            CONFIG['topic'], CONFIG['client_id']), bytes(str(DHT_PIN.humidity()), 'utf-8'))

        print('Temperature: {}, Humidity: {}'.format(DHT_PIN.temperature_f(), DHT_PIN.humidity()))
        time.sleep(CONFIG['sleep_seconds'])


if __name__ == '__main__':
    CONFIG = load_config()
    setup_pins()
    main()
