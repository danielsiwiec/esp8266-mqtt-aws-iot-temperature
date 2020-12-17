import network

def connect_to_wifi(sid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(sid, password)
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig())