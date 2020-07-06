<p align="left" >
<a href="https://github.com/RoberWare/wifiConf/graphs/contributors"><img src="https://img.shields.io/github/contributors/RoberWare/wifiConf" alt="Github contributors"/></a>
<!-- <a href="https://github.com/RoberWare/wifiConf"><img src="https://img.shields.io/github/release-pre/RoberWare/wifiConf" alt="Github release"/></a>
<a href="https://github.com/RoberWare/wifiConf/stargazers"><img src="https://img.shields.io/github/stars/RoberWare/wifiConf" alt="Github stars"/></a> -->
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

#### Description
*wifiConfig* is a flask app, for an easy wifi configuration.

#### Tested environments

|                         |                                         |
|-------------------------|-----------------------------------------|
| **Hardware**            | Rpi zero W                              | 
| **Operating systems**   | Linux                                   |
| **Python versions**     | Python 3.x                              |
| **Distros**             | Raspbian 10                             |
| **Languages**           | English                                 |

#### Instalation
```Shell
sudo pip3 install wifiConfig
```

#### Usage 
 - Terminal 
```Shell
sudo wifiConfig start
```
You need to run it with permissions to modify the file /etc/wpa_supplicant/wpa_supplicant.conf

```Shell
usage: wifiConfig [-h] [-w WLAN] [-i INET] [-ip IP] [-n NETMASK] [-s SSID]
                  [-p PASSWORD] [-ho HOST] [-po PORT]
                  {start}

A utility create a wifi hotspot on linux

positional arguments:
  {start}

optional arguments:
  -h, --help            show this help message and exit
  -w WLAN, --wlan WLAN  wi-fi interface that will be used to create hotspot
                        (default: wlan0)
  -i INET, --inet INET  forwarding interface (default: None)
  -ip IP                ip address of this machine in new network (default:
                        192.168.0.1)
  -n NETMASK, --netmask NETMASK
                        no idea what to put here as help, if don't know what
                        is it don't change this parameter (default:
                        255.255.255.0)
  -s SSID, --ssid SSID  name of new hotspot (default: MyAccessPoint)
  -p PASSWORD, --password PASSWORD
                        password that can be used to connect to created
                        hotspot (default: 1234567890)
  -ho HOST, --host HOST
                        name of new hotspot (default: 0.0.0.0)
  -po PORT, --port PORT
                        password that can be used to connect to created
                        hotspot (default: 8080)

```
 
 - Python
```Python
import wifiConfig
access_point_config = {"wlan":'wlan0', "inet":None, "ip":'192.168.0.1', "netmask":'255.255.255.0', "ssid":'MyAccessPoint', "password":'1234567890'}
flask_app_config = {"host":"0.0.0.0", "port":"8080"}
myWifiConfig = wifiConfig.WifiConfApp(access_point_config, flask_app_config)
myWifiConf.start()
```

By default it will create a hotspot called "MyAccessPoint", with password "1234567890" 
and the flask app running at http://192.168.0:8080 
You can change this with the parameters of the constructor.

#### Dependencies
- System dependencies
  - python3
- Python dependencies
    - PyAccessPoint, made by @Goblenus that uses https://pypi.org/project/hostpotd
    - flask
    
#### Mentions
  - PyAccessPoint, made by @Goblenus that uses https://pypi.org/project/hostpotd
  - python-wifi (modified) made by @CptMonac 
  
#### Developer
Roberto Lama Rodríguez - roberlama@gmail.com
 
