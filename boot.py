# ...module boot.py
# Create connection to trusted AP
from network import WLAN, STA_IF
import gc
from time import sleep_ms

from config import load_config


def try_connection():
    t = 12
    while not wlan.isconnected() and t > 0:
        print('.', end='')
        sleep_ms(500)
        t = t - 1
    return wlan.isconnected()


CONFIG = load_config

wlan = WLAN(STA_IF)
wlan.active(True)
print('connecting to last AP', end='')
print(try_connection())
if not wlan.isconnected():
    # find all APs
    ap_list = wlan.scan()
    # sort APs by signal strength
    ap_list.sort(key=lambda ap: ap[3], reverse=True)
    # filter only trusted APs
    ap_list = list(filter(lambda ap: ap[0].decode('UTF-8') in
                          CONFIG['wireless_networks'].keys()), ap_list)
    for ap in ap_list:
        essid = ap[0].decode('UTF-8')
        if not wlan.isconnected():
            print('Connecting to new AP', essid, end='')
            wlan.connect(essid, APS[essid])
            print(try_connection())


gc.collect()
