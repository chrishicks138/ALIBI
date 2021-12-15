class Keys():

    def __init__(self):

        self.wifikeys = [
                'bssid',
                'frequency_mhz',
                'rssi',
                'ssid',
                'timestamp',
                'channel_bandwidth_mhz',
                'center_frequency_mhz',
                'date',
                ]
        
        self.wifikeysedit = [
                'bssid',
                'frequency_mhz',
                'rssi',
                'ssid',
                'timestamp',
                'channel_bandwidth_mhz',
                'center_frequency_mhz',
                ]

        self.gpskeys = [
                'latitude',
                'longitude',
                'altitude',
                'accuracy',
                'vertical_accuracy',
                'bearing',
                'speed',
                'elapsedMs',
                'provider',
                ]
        self.gpskeysedit = [
                'latitude',
                'longitude',
                'date',
                'altitude',
                'accuracy',
                'vertical_accuracy',
                'bearing',
                'speed',
                'elapsedMs',
                'provider',
                'date',
                ]

        self.batterykeys = [
            'timestamp',
            'current',
            'temperature',
            'status',
            'percentage',
            'plugged',
            'health',
                ]

        self.sensorkeys = [
                'timestamp',
                'X',
                'Y',
                'Z',
                ]
