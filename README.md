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
|                         |                                         |

#### Instalation
       pip3 install --user wifiConf
  
#### Usage 

   > import wifiConf
 
 > myWifiConf = wifiConf.WifiConfApp()
 
 > myWifiConf.start()

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
 
