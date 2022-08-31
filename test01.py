# import gspread
# gc = gspread.service_account(filename='credentials.json')
# worksheet = gc.open_by_key('1xCmulH3mgkT31tzTfY7Yym3zx77S_BCrD-M_AHvBw3c')
# log= worksheet.sheet1
# res = log.update_cell(11,1,55)
# res = log.cell(11,1).value
# print(res)
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
print(type(config['Config']['GAP']))