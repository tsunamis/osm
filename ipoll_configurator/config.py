import json
import sys


def get_confige(NAME, IP, GATEWAY, FILE):
    #FILE='config_11ac.json'

    new_config = {}
    '''
    WIRELESS_MODE = 'ap'
    SSID = 'ipoll64'
    IPOLL_VERSION = 'ipollv3'
    NAME = "PtMP AP"
    IP = "192.168.2.66"
    GATEWAY = '192.168.2.27'
    vap_count = -1
    '''

    with open(FILE) as data_file:    
        config = json.load(data_file)

    '''
    def get_vap():
        return config['wireless']['radio'][0]['vap'][0].copy()

    def get_radio():
        r = config['wireless']['radio'][0].copy()
        r['vap'] = []
        return r

    new_config['network'] = config['network'].copy()
    new_config['services'] = config['services'].copy()
    new_config['wireless'] = config['wireless'].copy()
    #del new_config['wireless']['radio']
    new_config['wireless']['radio'] = []
    new_config['system'] = config['system'].copy()
    '''

    # For network
    config['network']['topology'] = str('bridge')
    config['network']['bridge']['management']['mode'] = str('static')
    config['network']['bridge']['management']['static']['ip'][0]['ip'] = str(IP)
    config['network']['bridge']['management']['static']['ip'][0]['prefix'] = int(24)
    config['network']['bridge']['management']['static']['gateway'] = str(GATEWAY)

    # For system
    config['system']['device']['contact'] = "mindaugas@wilibox.com"
    config['system']['device']['name'] = NAME
    config['system']['device']['coordinate']['latitude'] = 0
    config['system']['device']['coordinate']['longitude'] = 0
    config['system']['device']['location'] = "AutoTestlab2"

    '''
    # For wireless
    new_config['wireless']['countrycode'] = str('CT')


    #For 2G WIFI
    radio1 = None
    radio1 = get_radio()
    radio1['ieeemode'] = str('ac')
    radio1['channel']['width'] = int(80)
    radio1['channel']['select'] = str("list")
    radio1['channel']['list'] = [5180]
    radio1['ifname'] = str('wifi0')
    radio1['wjet']['enabled'] = bool(True)
    radio1['wjet']['version'] = str(IPOLL_VERSION)
    radio1['txpower'] = 17

    new_config['wireless']['radio'].append(radio1)

    for i in range(1):
        vap1 = None
        vap_count += 1

        vap1 = get_vap()
        vap1['cwm'] = bool(False)
        vap1['ifname'] = str('ath%s' % vap_count)
        vap1['mode'] = str(WIRELESS_MODE)
        #vap1['ssid'] = str('%s-%s' % (SSID, vap_count))
        vap1['ssid'] = str('SSID')
        vap1['wds'] = bool(True)
        vap1['wmm'] = bool(True)
        radio1['vap'].append(vap1)
        print "%s !!! %s" % (i, vap_count)

    #For 2/5G WIFI
    radio1 = None
    radio1 = get_radio()
    radio1['ieeemode'] = str('ac')
    radio1['channel']['width'] = int(80)
    radio1['ifname'] = str('wifi1')
    new_config['wireless']['radio'].append(radio1)

    for i in range(1):
        vap1 = None
        vap_count += 1

        vap1 = get_vap()
        vap1['cwm'] = bool(False)
        vap1['ifname'] = str('ath%s' % vap_count)
        vap1['mode'] = str('ap')
        vap1['ssid'] = str('%s-%s' % (SSID, vap_count))
        vap1['wds'] = bool(True)
        vap1['wmm'] = bool(True)
        radio1['vap'].append(vap1)
        print "%s !!! %s" % (i, vap_count)


    #For 2G WIFI
    radio1 = None
    radio1 = get_radio()
    radio1['ieeemode'] = str('auto')
    radio1['ifname'] = str('wifi2')
    new_config['wireless']['radio'].append(radio1)

    for i in range(1):
        vap1 = None
        vap_count += 1

        vap1 = get_vap()
        vap1['cwm'] = bool(False)
        vap1['ifname'] = str('ath%s' % vap_count)
        vap1['mode'] = str('sta')
        vap1['ssid'] = str('klausausi')
        radio1['vap'].append(vap1)
        print "%s !!! %s" % (i, vap_count)


    #print json.dumps(config['wireless']['radio'][0]['vap'][0]['wds'], indent=4,  sort_keys=True)
    #print json.dumps(config['wireless']['radio'][0], indent=4,  sort_keys=True)
    #print json.dumps(new_config['network']['bridge']['management']['static']['ip'][0], indent=4,  sort_keys=True)
    '''

    f = open('/tmp/oem.json', 'w')
    f.write(json.dumps(config, indent=4, sort_keys=True))
