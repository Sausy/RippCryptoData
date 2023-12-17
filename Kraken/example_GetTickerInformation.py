#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Dez 6 2023

@author: sausy
"""

import requests 
import time
import datetime



class kraken:
    def __init__(self, currencySymbol="BTCUSD", api_start="1483225200", api_end="9999999999"):
        #default values
        self._api_domain = "https://api.kraken.com"
        self._api_path = "/0/public/"
        self.api_method = ""  # eg.: Trades, Time, SystemStatus
        self.api_data = ""
        self.api_start = api_start
        self.api_end = api_end  # "9999999999"

        # fix input
        self.api_symbol = currencySymbol.upper()
        
    
    def build_req(self):
        api_request = self._api_domain + self._api_path + self.api_method + self.api_data 
        return api_request
    
    def get_ServerTime(self):
        ## Get Server Time
        # {'error': [], 'result': {}}
        #
        # unixtime  -> integer |  Unix timestamp
        # rfc1123   -> string  |  RFC 1123 time format
        self.api_method = "Time"
        self.api_data = ""

        # send request to Server
        resp = requests.get(self.build_req())
        print("Server Time, ", resp.json())

        

    def get_ServerStatus(self):
        ## Get System Status
        # {'error': [], 'result': {}}
        #
        # status    -> string |  Enum: "online" "maintenance" "cancel_only" "post_only"
        self.api_method = "SystemStatus"
        self.api_data = ""

        # send request to Server
        resp = requests.get(self.build_req())
        print("Server Status, ", resp.json()) 
    
    def get_TradeInfo(self):
        ## Get Trade info
        #like leverage, fees, margins, ... 
        self.api_method = "AssetPairs"
        self.api_data = "?pair=%(pair)s" % {"pair": self.api_symbol}

    def get_OrderBook(self): 
        ## Get Order Book
        self.api_method = "Depth"
        self.api_data = "?pair=%(pair)s" % {"pair": self.api_symbol}

        # send request to Server
        resp = requests.get(self.build_req())
        print("Server Status, ", resp.json())
    
    def get_TickerInformation(self):
        ## Get Ticker Information
        # {'error': [], 'result': {}}
        #
        # a   ->  Array of strings    | Ask [<price>, <whole lot volume>, <lot volume>]
        # b   ->  Array of strings    | Bid [ < price > , < whole lot volume > , < lot volume > ]
        # c   ->  Array of strings    | Last trade closed [< price > , < lot volume > ]
        # v   ->  Array of strings    | Volume [< today > , < last 24 hours > ]
        # p   ->  Array of strings    | Volume weighted average price [< today > , < last 24 hours > ]
        # t   ->  Array of integers   | Number of trades [< today > , < last 24 hours > ]
        # l   ->  Array of strings    | Low [< today > , < last 24 hours > ]
        # h   ->  Array of strings    | High [< today > , < last 24 hours > ]
        # o   ->  string              | Today's opening price
        # error -> Array of strings(error)
        self.api_method = "Ticker"
        self.api_data = "?pair=%(pair)s" % {"pair": self.api_symbol}

        # send request to Server
        resp = requests.get(self.build_req())
        print(resp.json())
    
    def get_TradeInformation(self):
        ## Get Trade Information
        # {'error': [], 'result': {"*pair*:{}, last:''}}
        #
        # 'pair'->  Array of trade entries [<price>, <volume>, <time>, <buy/sell>, <market/limit>, <miscellaneous>, <trade_id>]
        # error ->  Array of strings(error)
        self.api_method = "Trades"
        self.api_data = "?pair=%(pair)s&since=%(since)s&count=%(count)s" % {
            "pair": self.api_symbol, "since": self.api_start, "count": 10}

        # send request to Server
        resp = requests.get(self.build_req())
        print(resp.json())


# time.struct_time(
# tm_year=2018, tm_mon=12, tm_mday=27,
# tm_hour=6, tm_min=35, tm_sec=17,
# tm_wday=3, tm_yday=361, tm_isdst=0)

# the 1.1.2017 was a sunday
# and tm_yday=1 because it was the first day of the year
#startTime_ = (2017, 1, 1, 0, 0, 0, 6, 1, 0)
#startTime = int(time.mktime(startTime_))
#print(datetime.timedelta(minutes=5))
#print(time.mktime(datetime.timedelta(minutes=5)))

print(time.time())

startTime = int(time.time()) - 1000
endTime = int(time.time())

print(startTime)
print(endTime)
print("pull StartTime: \t{}".format(time.ctime(startTime)))
print("pull EndTime: \t{}".format(time.ctime(endTime)))

krak = kraken("XXBTZUSD", str(startTime), str(endTime))

krak.get_ServerTime()
krak.get_ServerStatus()
krak.get_TickerInformation()
krak.get_TradeInformation()
