#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
from wifiConfig.scripts.wifi import Finder, Cell


#***GLOBAL VARS***
wlan='wlan0'
app = Flask("wifi_conf",
            static_url_path='/static')
os.environ["PYTHONOPTIMIZE"] = "1"
thr_connect = None
myWifiConf = None
