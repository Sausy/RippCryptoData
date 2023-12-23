#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Dez 22 2023

@author: sausy
"""

import requests 
import time
import datetime


class kraken:
    def __init__(self, base="BTC", quote='USD' , api_start="1483225200", api_end="9999999999"):
        #default values
        self._api_domain = "https://api.kraken.com"
        self._api_path = "/0/public/"
        self.api_method = ""  # eg.: Trades, Time, SystemStatus
        self.api_data = ""
        self.api_start = api_start
        self.api_since = api_start
        self.api_end = api_end  # "9999999999"

        # set Asset Pair 
        self.api_symbol =  ""
        self.set_pairName(base, quote)
        
    
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
    
    def set_pairName(self, base, quote):
        asset_pair = base + quote
        self.api_symbol = asset_pair.upper()  
        ticker = self.get_TickerInformation()

        # lets correct the api_symbol
        self.api_symbol = list(ticker['result'].items())[0][0]

    
    def get_AssetPairs(self, base, quote):
        ## Get Trade info
        #like leverage, fees, margins, ... 
        self.api_method = "AssetPairs"
        self.api_data = "?pair=%(base)s/%(quote)s" % {"base": base, "quote": quote}
        print(self.api_data)
        resp = requests.get(self.build_req()).json()
        print("AssetPairTag: , ", resp)

    def get_AssetInfo(self, base, quote):
        ## Get Asset 
        # e.g.: Bitcoin and USD will return as XXBTZUSD
        self.api_method = "Assets"
        self.api_data = "?asset=%(base)s,%(quote)s" % {"base": base, "quote": quote}
        resp = requests.get(self.build_req()).json()
        print("AssetPairTag: , ", resp)

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
        resp = requests.get(self.build_req()).json()
        return resp
    
    def get_TradeInformation(self):
        ## Get Trade Information
        # {'error': [], 'result': {"*pair*:{}, last:''}}
        #
        # 'pair'->  Array of trade entries [<price>, <volume>, <time>, <buy/sell>, <market/limit>, <miscellaneous>, <trade_id>]
        # error ->  Array of strings(error)
        count_ = 100 # 2 trades per request 

        self.api_since = self.api_start
        self.api_method = "Trades"

        for i in range(0, 20):
            self.api_data = "?pair=%(pair)s&since=%(since)s&count=%(count)s" % {
                "pair": self.api_symbol, "since": self.api_since, "count": count_}

            # send request to Server
            resp = requests.get(self.build_req()).json()

            # update since, the get the next batch of trades
            self.api_since = resp['result']['last']
            print('last: ', self.api_since)
            print("data: ", len(resp['result'][self.api_symbol]))

            if len(resp['result'][self.api_symbol]) < count_:
                print("End reached")
                break

 

print(time.time())

now = datetime.datetime.now() 

endTime = int(now.timestamp())
startTime = int((now - datetime.timedelta(minutes=20)).timestamp())


print("Now: ", endTime)
print("Now2: ", int(time.time()))
print(endTime)
print("pull StartTime: \t{}".format(time.ctime(startTime)))
print("pull EndTime: \t{}".format(time.ctime(endTime)))

krak = kraken("BTC", "USD", str(startTime), str(endTime))

krak.get_ServerTime()
krak.get_ServerStatus()
krak.get_TickerInformation()
print("========[get_TradeInformation]=============")
krak.get_TradeInformation()
