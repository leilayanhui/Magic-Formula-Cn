import tushare as ts

def getToday():
    '''从tushare获取当天报价表'''
    data = ts.get_today_all()
    data.to_excel('today.xls')

getToday()
