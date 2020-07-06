import os
import subprocess
import re
import textwrap

class Cell(object):
    """
    Presents a Python interface to the output of iwlist.
    """

    def __init__(self):
        self.bitrates = []

    def __repr__(self):
        return 'Cell(ssid={ssid})'.format(**vars(self))

    @classmethod
    def all(cls, interface):
        """
        Returns a list of all cells extracted from the output of
        iwlist.
        """
        iwlist_scan = subprocess.check_output(['/sbin/iwlist', interface, 'scan']).decode('utf-8')

        cells = map(normalize, cells_re.split(iwlist_scan)[1:])

        return cells

    @classmethod
    def where(cls, interface, fn):
        """
        Runs a filter over the output of :meth:`all` and the returns
        a list of cells that match that filter.
        """
        return list(filter(fn, cls.all(interface)))


class Finder:
    def __init__(self, server_name=None, password=None, interface=None, country='ES'):
        self.server_name = server_name
        self.password = password
        self.interface = interface
        self.country=country
        self.main_dict = {}
        #print(self.server_name,self.password)
    def find(self):
        iwlist_scan = subprocess.check_output(['/sbin/iwlist', self.interface, 'scan']).decode('utf-8')

        cells = map(normalize, cells_re.split(iwlist_scan)[1:])

        w_list=[]
        for w in list(cells):
            if w.ssid != "":
                w_list.append({"ssid":w.ssid, "signal":w.signal, "quality":w.quality, "frequency":w.frequency, 
                               "bitrates":w.bitrates, "encrypted":w.encrypted, "channel":w.channel, 
                               "address":w.address, "mode":w.mode})
        return w_list


    def run(self):
        command = """/sbin/iwlist %s scan | grep -ioE 'ssid:"(.*{}.*)'"""%(self.interface)
        result = os.popen(command.format(self.server_name))
        result = list(result)
        #print(result)
        if "Device or resource busy" in result:
                return None
        else:
            ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]
            print("Successfully get ssids {}".format(str(ssid_list)))

        for name in ssid_list:
            try:
                result = self.connection(name)
            except Exception as exp:
                print("Couldn't connect to name : {}. {}".format(name, exp))
            else:
                if result:
                    print("Successfully connected to {}".format(name))

    def reset(self):
        os.system("sudo pyaccesspoint stop")
        new_f="""
            auto lo
            iface lo inet loopback

            auto %s
            #allow-hotplug %s
            iface %s inet dhcp
            wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
        """%(self.interface,self.interface,self.interface)
        with open("/etc/network/interfaces", "w+") as f:
            f.write(new_f)
            
        new_f="""
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        country=%s
        """%(self.country)
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w+") as f:
            f.write(new_f)
        #os.system("sudo ifdown wlan0")


    def connection(self):
        self.reset()
        #try:
        os.system("sudo su -c 'wpa_passphrase %s %s >> /etc/wpa_supplicant/wpa_supplicant.conf'"%(self.server_name,self.password))
        os.system("wpa_cli -i %s reconfigure"%(self.interface))
        os.system("sudo ifdown wlan0 && sudo ifup wlan0")
        #except:
        #    raise
        #else:
        #    return True
        
        
        
        #new_f="""
        #    auto lo
        #    iface lo inet loopback

        #    auto wlan0
        #    iface wlan0 inet dhcp
        #        wpa-ssid %s
        #        wpa-psk %s
        #"""%(self.server_name,self.password)
        #with open("/etc/network/interfaces", "a") as f:
        #    f.write(new_f)
        #os.system("sudo ifdown wlan0 && sudo ifup wlan0")

cells_re = re.compile(r'Cell \d+ - ')
quality_re = re.compile(r'Quality=(\d+/\d+).*Signal level=(-\d+) dBm')
frequency_re = re.compile(r'([\d\.]+ .Hz).*')


scalars = (
    'address',
    'channel',
    'mode',
)

identity = lambda x: x

key_translations = {
    'encryption key': 'encrypted',
    'essid': 'ssid',
}


def normalize_key(key):
    key = key.strip().lower()

    key = key_translations.get(key, key)

    return key.replace(' ', '')

normalize_value = {
    'ssid': lambda v: v.strip('"'),
    'frequency': lambda v: frequency_re.search(v).group(1),
    'encrypted': lambda v: v == 'on',
    'channel': int,
    'address': identity,
    'mode': identity,
}


def split_on_colon(string):
    key, _, value = map(lambda s: s.strip(), string.partition(':'))

    return key, value


def normalize(cell_block):
    """
    The cell blocks come in with the every line except the first
    indented 20 spaces.  This will remove all of that extra stuff.
    """
    lines = textwrap.dedent(' ' * 20 + cell_block).splitlines()
    cell = Cell()

    while lines:
        line = lines.pop(0)

        if line.startswith('Quality'):
            cell.quality, cell.signal = quality_re.search(line).groups()
        elif line.startswith('Bit Rates'):
            values = split_on_colon(line)[1].split('; ')

            # consume next line of bit rates, because they are split on
            # different lines, sometimes...
            while lines[0].startswith(' ' * 10):
                values += lines.pop(0).strip().split('; ')

            cell.bitrates.extend(values)
        elif ':' in line:
            key, value = split_on_colon(line)
            key = normalize_key(key)

            if key == 'ie':
                if 'Unknown' in value:
                    continue

                # consume remaining block
                values = [value]
                while lines and lines[0].startswith(' ' * 4):
                    values.append(lines.pop(0).strip())

                for word in values:
                    if 'WPA2' in word:
                        cell.encryption_type = 'wpa2-?'
                    elif 'PSK' in word:
                        cell.encryption_type = 'wpa2-psk'
                    elif '802.1x' in word:
                        cell.encryption_type = 'wpa2-eap'
            elif key in normalize_value:
                setattr(cell, key, normalize_value[key](value))
    return cell
    

