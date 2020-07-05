"""
*******************************
*                             *
*         wifiConfig          *
*                             * 
*******************************

Description
    Flask app, for an easy wifi configuration

Modules
    PyAccessPoint that uses https://pypi.org/project/hostpotd
    python-wifi modified

Developer
    Roberto Lama Rodríguez
    roberlama@gmail.com
"""


#***MODULES***
import sys,os,time,argparse
from threading import Thread
from multiprocessing import Process, Value
import urllib.request as urllib2
from flask import Flask, request, redirect, url_for, g
from PyAccessPoint import pyaccesspoint
if __name__ == "__main__":
    from scripts.wifi import Finder, Cell
else:
    from wifiConfig.scripts.wifi import Finder, Cell

#***GLOBAL VARS***
wlan='wlan0'
app = Flask("wifi_conf",
            static_url_path='/static')
os.environ["PYTHONOPTIMIZE"] = "1"
thr_connect = None
myWifiConf = None

class WifiConfApp():
    """
        Main app
            @description
                Uses the main class to create the access point and the flask app,
                also stop the flask app when the wifi is connected.
            @params 
                access_point
                    one dict with the following keys: wlan, inet, ip, netmask, ssid, password
                    will be passed to pyAccessPoint
                flask_app
                    another dict with keys: host and port
                    will be passed to our flask app
    """
    def __init__(self, access_point = {
                            "wlan":'wlan0', "inet":None, "ip":'192.168.0.1', "netmask":'255.255.255.0', 
                            "ssid":'MyAccessPoint', "password":'1234567890'},
                       flask_app = {
                            "host":"0.0.0.0", "port":"8080"}):
        self.connected = Value('i', 0)
        global myWifiConf
        myWifiConf = WifiConf(access_point, flask_app, self.connected)
        
    def start(self):
        main = Process(target = myWifiConf.start)
        main.start()
        while True:
            myWifiConf.reset_ap()
            self.connected.value=0
            while self.connected.value != 1:
                #print("waiting "+str(self.connected.value)) 
                time.sleep(5)
            #global thr_connect
            #print(thr_connect)
            #thr_connect.join()
            print("finished")
            print("checking network...")
            if myWifiConf.check_con():
                print("network checked")
                break
            else:
                print("ERROR: network without internet conn")
        main.terminate()
        main.join()
        
#***MAIN CLASS***
class WifiConf():
    """
        Main class
            @params 
                access_point
                    one dict with the following keys: wlan, inet, ip, netmask, ssid, password
                    will be passed to pyAccessPoint
                flask_app
                    another dict with keys: host and port
                    will be passed to our flask app
    """
    def __init__(self, access_point,flask_app,connected):
        if connected != None: 
            self.connected=connected
            self.connected.value=0
        self.host=flask_app["host"]
        self.port=flask_app["port"]
        self.wlan=access_point["wlan"]
        global wlan
        wlan=self.wlan
        self.access_point = pyaccesspoint.AccessPoint(wlan=access_point["wlan"],
                                             ip=access_point["ip"],
                                             inet=access_point["inet"],
                                             ssid=access_point["ssid"],
                                             netmask=access_point["netmask"],
                                             password=access_point["password"])
                                             
    def connect(self,req, server_name, pw):
        with app.test_request_context():
            request = req
            time.sleep(1)
            self.access_point.stop()
            os.system("sudo pyaccesspoint stop")   
            myFinder=Finder(server_name=server_name,
                            password=pw,
                            interface=self.wlan) 
            myFinder.connection()
            self.connected.value=1
            print("connected!")
        print("ok")

    def reset_ap(self):
        os.system("sudo pyaccesspoint stop")    
        self.access_point.start()
                

    def start(self):
        try:
            print("running? "+str(self.access_point.is_running()))
            app.run(host=self.host, port=self.port)
        
        except Exception as e:
            print(e)
            sys.exit()

    def check_con(self):
        try:
            urllib2.urlopen("http://www.google.com",timeout=1)
            return True
        except:
            return False

#***FLASK APP***
def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f
    
@app.after_request
def call_after_request_callbacks(response):
    for callback in getattr(g, 'after_request_callbacks', ()):
        callback(response)
    return response

@app.route("/")
def wifi_conf_page():
    html = """
           <html>
                <header>
                    <title>Wifi conf</title>
                     <link rel="stylesheet" href="/static/css/style.css">
                    <script src="/static/js/main.js"></script> 
                </header>
                <body>
                    <form action="/connect" method="post" class="login-form">
                        <h1>Wifi conf</h1>
           """ 
    for i in range(3):
        try:
            myFinder=Finder(interface=wlan)
            ans=myFinder.find()
            if ans != []:
                break
            else:
                print("empty list")
        except Exception as e:
            print(e)
    if ans != []:
        html+="""
                        <div class="form-input-material">
                            <a>SSID</a>
                            <select name="ssid">
                """
        for w in ans:
            html+="""
                                    <option value="%s">%s</option>
                  """%(w["ssid"],w["ssid"])
              
                  
        html+="""
                                </select>
                        </div>
                          <div class="form-input-material">
                            <label for="password">Password</label>
                            <input type="password" name="password" id="password" placeholder=" " autocomplete="off" class="form-control-material" required />
                          </div>
                          <button type="submit" class="btn btn-primary btn-ghost">Login</button>
                          
               """
    else:
        html+="No networks avaiable."          
    html+="""
                    </form>
              </body>
          </html>
          """
    return html


@app.route("/connect", methods=['POST'])
#@app.before_request
def connect_page():
    server_name=request.form.get("ssid")
    pw=request.form.get("password")    
    global thr_connect
    thr_connect = Thread(target=myWifiConf.connect, args=[request, server_name, pw])
    thr_connect.start()
    return "connecting..."
    
@app.route('/shutdown', methods=['POST'])
def shutdown():
    fin = request.environ.get('werkzeug.server.shutdown')
    fin()
    return 'Shutdown...'


def main():
    parser = argparse.ArgumentParser(description='A utility create a wifi hotspot on linux',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('command', choices=['start'])
    parser.add_argument('-w', "--wlan", required=False, default='wlan0',
                        help='wi-fi interface that will be used to create hotspot')
    parser.add_argument('-i', "--inet", required=False, default=None, help='forwarding interface')
    parser.add_argument('-ip', required=False, default='192.168.0.1', help='ip address of this machine in new '
                                                                            'network')
    parser.add_argument('-n', "--netmask", required=False, default='255.255.255.0',
                        help='no idea what to put here as help, if don\'t know what is it don\'t change this parameter')
    parser.add_argument('-s', "--ssid", required=False, default='MyAccessPoint', help='name of new hotspot')
    parser.add_argument('-p', "--password", required=False, default='1234567890',
                        help='password that can be used to connect to created hotspot')

    parser.add_argument('-h', "--host", required=False, default='0.0.0.0', help='name of new hotspot')
    parser.add_argument('-po', "--port", required=False, default='8080',
                        help='password that can be used to connect to created hotspot')

    args = parser.parse_args()
    
    if args.command == 'start':
        myWifiConfApp = WifiConfApp()
        myWifiConfApp.start()

if __name__ == "__main__":
    sys.exit(main())
