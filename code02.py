import time
import requests
import json
import os

#Config
# from configparser import ConfigParser
# config = ConfigParser()
# config.read('test02\config.ini')

#Google Sheet
# import gspread
# gc = gspread.service_account(filename ='test02\credentials.json')
# worksheet = gc.open_by_key('1xCmulH3mgkT31tzTfY7Yym3zx77S_BCrD-M_AHvBw3c')
# log= worksheet.sheet1

# การส่ง Line
from line_notify import LineNotify  
# Line_Notify = config['Config']['LineNotify']
Line_Notify = str(os.environ['LineNotify']) 
notify = LineNotify(Line_Notify)

# Login
from bitkub import Bitkub
API_HOST = 'https://api.bitkub.com/'
# API_KEY = config['Config']['API_KEY']
API_KEY = str(os.environ['API_KEY']) 
# API_SECRET = config['Config']['API_SECRET']
API_SECRET = str(os.environ['API_SECRET']) 


Account_name  = "RB_50/50_TEST00"
# SetAsset =  config['Config']['Asset']
SetAsset = str(os.environ['Asset']) 
Asset = SetAsset.split(",")
# SetCoo =  config['Config']['Core']
SetCoo = str(os.environ['Core']) 
coo = SetCoo.split(",")
# DCA = int(config['Config']['DCA'])
DCA = str(os.environ['DCA']) 
# GAP = float(config['Config']['GAP'])
GAP = str(os.environ['GAP']) 
Bot=" "

try:
    for i in range(len(Asset)):
        if log.cell(1, i + 2) != Asset[i]:    #update value
            log.update_cell(6,i + 1,Asset[i])
            log.update_cell(7,i + 1,int(coo[i]))
            log.update_cell(8,i + 1,int(coo[i]))

        elif log.cell(3, i + 2).value != int(coo[i]):
            Asset[i] = log.cell(6,i + 1).value
            coo[i] = log.cell(7, i + 1).value
            coo[i] = log.cell(8, i + 1).value

except Exception as e:
    print(e)
    print('Close in 60s')
    time.sleep(60)

Account_name = "JK & L1NEMAN\n(・ᴥ・) Bot v.2.3.1"
password = ""

t = 1
start = time.time()

while True :
    h = 0
    while (h < 12): # from 24 hr to 12 hr
        n = 0
        while (n < 60):
            try:
                bitkub = Bitkub()
                bitkub.set_api_key(API_KEY)
                bitkub.set_api_secret(API_SECRET)
                bitkub.status()
                bitkub.servertime()
                res = 'result'
                
                if t == 1:
                  notify.send(Account_name, sticker_id=17851, package_id=1070)
                  t = 0
                else:
                  t = 0
                  
                if Account_name == "":
                    print("\n""Account Name - This is Main Account", ': Broker - ', 'Bitkub')
                else:
                    print("\n"'Account Name - ', Account_name, ': Broker - ', 'Bitkub')

                Get_balance = bitkub.wallet()

                for i in range(len(Asset)):
                    Core = log.cell(3, i + 2).value #
                    Asset_01 = Get_balance[res][Asset[i]]
                    AssetName = 'THB_' + Asset[i]
                    get_price = bitkub.ticker(AssetName)
                    Asset_01_Value = Asset_01 * get_price[AssetName]['last']
                    print(Asset_01, Asset[i], '=', "{:.2f}".format(Asset_01_Value), '฿ <==> ฿', Core)
                    rat = get_price[AssetName]['last']
                    CoreAsset = int(Core)
                    if CoreAsset > 600:
                        if GAP > 2:
                          Rebalance_percent = GAP
                        else:
                          Rebalance_percent = 2
                    
                    else:
                        Rebalance_percent = 1200 / CoreAsset
                        DiffAsset = (CoreAsset * Rebalance_percent / 100)
                    if Asset_01_Value > (CoreAsset + DiffAsset):
                        if DiffAsset > 200:
                          diff_sell = DiffAsset - 4
                        elif DiffAsset > 100:
                          diff_sell = DiffAsset * .98
                        elif DiffAsset > 50:
                          diff_sell = DiffAsset - 1.5
                        else:
                          diff_sell = int(DiffAsset) - 1
                          bitkub.place_ask_by_fiat(sym=AssetName, amt=diff_sell, rat=rat, typ='market')
                          coo[i] = float(Core + GAP)  # ขยายพอร์ตเมื่อมีการขาย ทีละ 5฿"
                          notify.send('\nESP32:Sell_' + str(AssetName) + '\nCore = ฿' + Core+5,sticker_id=2009, package_id=446)
                          print("ESP32:SELL_" + str(diff_sell) + " ฿")
                          log.update_cell(3,i + 2,str(Core + GAP))
                          log.update_cell(7,i + 1,str(Core + GAP))
                          log.update_cell(8,i + 1,str(Core + GAP))
                          

                    elif Asset_01_Value < (CoreAsset - (CoreAsset * Rebalance_percent / 100)):
                      diff_buy = CoreAsset * Rebalance_percent / 100
                      bitkub.place_bid(sym=AssetName, amt=diff_buy, rat=rat, typ='market')
                      print("ESP32:Buy_" + str(diff_buy) + " ฿")
                      notify.send('\nESP32:Buy_' + str(AssetName),sticker_id=2003, package_id=446)

                    else:
                      print('ESP32:Diff_'"{:.2f}".format(Asset_01_Value - CoreAsset), '฿')
                n += 1
                Bot = '\nESP32:Cash_ ฿ ' + str('{:.2f}'.format(Get_balance[res]['THB']))
                print(Bot)
                rows = log.get_all_values()
                sleep = 60
                time.sleep(sleep)  # Delay for 1 minute (60 seconds).
                end = time.time()
                if (end  - start)//1 == 3600:
                  notify.send("\n 1 hr. is pass \n")
                  start = end

            except Exception as e:
                print(e)
                try:
                  notify.send(e)
                except Exception as e:
                  print(e)
                  pass
                pass
        h += 1
        notify.send(Bot + "\nESP32: I am OK.")
        notify.send(Bot + "\nESP32: I am OK.", sticker_id=52002740, package_id=11537)
      
    for i in range(len(Asset)):
      Core = coo[i].value + int(DCA)  # ขยายพอร์ตทุก 12 ชม. (DCA)
      rows = log.get_all_values()
      log.update_cell(2,i+2,coo[i]+ int(DCA))
      print(Asset[i], str(Core))
      try:
        notify.send(Asset[i] + ' = ฿' + str(Core))
      except Exception as e:
        print(e)
        pass
