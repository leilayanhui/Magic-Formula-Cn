# -*- conding: utf-8 -*-
# config.py
import os
import re
basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SESSION_TYPE = 'sqlalchemy'

#__init__.py
import json
from flask import Flask
# from sqlalchemy import create_engine,and_
from flask_script import Manager,Shell
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session,SqlAlchemySessionInterface

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
db = SQLAlchemy(app)

def make_shell_context():
    return dict(app=app, db=db, BasicTable=BasicTable)

manager.add_command("shell", Shell(make_context=make_shell_context))

# 可在本地或后台操作
#import tushare as ts

#def getToday():
#    '''从tushare获取当天报价表'''
#    data = ts.get_today_all()
#    data.to_excel('today.xls')

# --------basicModels.py文件分割线--------
from datetime import datetime,date,timedelta
import xlrd

class BasicTable(db.Model):
    __tablename__ = 'basicTable'
    id = db.Column(db.Integer, primary_key = True)
    lastTime = db.Column(db.DateTime,index=True,default=datetime.utcnow) #更新时间
    code = db.Column(db.String(64)) #代码
    name = db.Column(db.String(64)) #名称
    industry = db.Column(db.String(64)) #所属行业
    income1 = db.Column(db.Integer) #1季度净利润
    income2 = db.Column(db.Integer) #2季度净利润
    income3 = db.Column(db.Integer) #3季度净利润
    income4 = db.Column(db.Integer) #4季度净利润
    incometax1 = db.Column(db.Integer) #1季度所得税
    incometax2 = db.Column(db.Integer) #2季度所得税
    incometax3 = db.Column(db.Integer) #3季度所得税
    incometax4 = db.Column(db.Integer) #4季度所得税
    finanExp1 = db.Column(db.Integer) #1季度财务费用
    finanExp2 = db.Column(db.Integer) #2季度财务费用
    finanExp3 = db.Column(db.Integer) #3季度财务费用
    finanExp4 = db.Column(db.Integer) #4季度财务费用
    THEquity = db.Column(db.Integer) #所有者权益合计
    iAssets = db.Column(db.Integer) #无形资产
    goodwill = db.Column(db.Integer) #商誉
    totals = db.Column(db.Integer) #总股本
    TLiab = db.Column(db.Integer) #负债合计
    mktcap = db.Column(db.Integer) #总市值


    def __repr__(self):
        return '<basicTable %r>' % self.name


class TodayTable(db.Model):
    __tablename__ = 'todayTable'
    id = db.Column(db.Integer, primary_key = True)
    lastTime = db.Column(db.DateTime,index=True,default=datetime.utcnow) #更新时间
    code = db.Column(db.String(64)) #代码
    name = db.Column(db.String(64)) #名称
    changepercent = db.Column(db.Integer) #涨跌幅
    trade = db.Column(db.Integer) #现价
    open = db.Column(db.Integer) #开盘价
    high = db.Column(db.Integer) #最高价
    low = db.Column(db.Integer) #最低价
    settlement = db.Column(db.Integer) #昨日收盘价
    volume = db.Column(db.Integer) #成交量
    turnoverratio = db.Column(db.Integer) #换手率
    amount = db.Column(db.Integer) #成交量
    per = db.Column(db.Integer) #市盈率
    pb = db.Column(db.Integer) #市净率
    mktcap = db.Column(db.Integer) #总市值
    nmc = db.Column(db.Integer) #流通市值

    def __repr__(self):
        return '<basicTable %r>' % self.name

def getData(filename,sheet):
    data = xlrd.open_workbook(filename)
    table = data.sheet_by_name(sheet)
    return table

class BasicModel(object):
    '''基础数据入库模块'''
    def __init__(self,filename,sheet):
        self.filename = filename #导入文件名
        self.sheet = sheet #导入表单名

    def insert(self):
        table = getData(self.filename,self.sheet)
        nrows = table.nrows
        for i in range(3,nrows):
            line = table.row_values(i)
            record = BasicTable(code = line[1],
                                name = line[2],
                                industry = line[3],
                                income1 = line[4], #1季度净利润
                                income2 = line[5], #2季度净利润
                                income3 = line[6], #3季度净利润
                                income4 = line[7], #4季度净利润
                                incometax1 = line[8], #1季度所得税
                                incometax2 = line[9], #2季度所得税
                                incometax3 = line[10], #3季度所得税
                                incometax4 = line[11], #4季度所得税
                                finanExp1 = line[12], #1季度财务费用
                                finanExp2 = line[13], #2季度财务费用
                                finanExp3 = line[14], #3季度财务费用
                                finanExp4 = line[15], #4季度财务费用
                                THEquity = line[16], #所有者权益合计
                                iAssets = line[17], #无形资产
                                goodwill = line[18], #商誉
                                totals = line[19], #总股本
                                TLiab = line[20]) #负债合计
            db.session.add(record)
            db.session.commit()

    def updateReport(self):
        table = getData(self.filename,self.sheet)
        nrows = table.nrows
        for i in range(3,nrows):
            line = table.row_values(i)
            record = BasicTable.query.filter_by(code = line[1]).first()
            if record is not None:
                record.income1 = line[4] #1季度净利润
                record.income2 = line[5] #2季度净利润
                record.income3 = line[6] #3季度净利润
                record.income4 = line[7] #4季度净利润
                record.incometax1 = line[8] #1季度所得税
                record.incometax2 = line[9] #2季度所得税
                record.incometax3 = line[10] #3季度所得税
                record.incometax4 = line[11] #4季度所得税
                record.finanExp1 = line[12] #1季度财务费用
                record.finanExp2 = line[13] #2季度财务费用
                record.finanExp3 = line[14] #3季度财务费用
                record.finanExp4 = line[15] #4季度财务费用
                db.session.add(record)
                db.session.commit()

    def updateToday(self):
        table = getData(self.filename,self.sheet)
        nrows = table.nrows
        for i in range(2,nrows):
            line = table.row_values(i)
            record = BasicTable.query.filter_by(code = line[1]).first()
            if record is not None:
                record.mktcap = line[14] #总市值
                db.session.add(record)
                db.session.commit()

class TodayModel(object):
    '''日报数据入库模块'''
    def __init__(self,filename,sheet):
        self.filename = filename #导入文件名
        self.sheet = sheet #导入表单名

    def insert(self):
        table = getData(self.filename,self.sheet)
        nrows = table.nrows
        for i in range(2,nrows):
            line = table.row_values(i)
            record = TodayTable(code = line[1],
                                name = line[2],
                                changepercent = line[3], #涨跌幅
                                trade = line[4], #现价
                                open = line[5], #开盘价
                                high = line[6], #最高价
                                low = line[7], #最低价
                                settlement = line[8], #昨日收盘价
                                volume = line[9], #成交量
                                turnoverratio = line[10], #换手率
                                amount = line[11], #成交量
                                per = line[12], #市盈率
                                pb = line[13], #市净率
                                mktcap = line[14], #总市值
                                nmc = line[15]) #流通市值
            db.session.add(record)
            db.session.commit()

def getMFData():
    '''获取神奇公式计算结果'''
    result = BasicTable.query.all()
    data_list = []
    for r in result:
        if r.mktcap is not None:
            ebitev = (r.income1 + r.income2 + r.income3 + r.income4 \
                    + r.incometax1 + r.incometax2 + r.incometax3 +  r.incometax4 \
                    + r.finanExp1 + r.finanExp2 + r.finanExp3 + r.finanExp4)/(r.mktcap + r.TLiab)
            # print(ebitev)
            if r.THEquity != 0:
                ROI = (r.income1 + r.income2 + r.income3 + r.income4\
                    + r.incometax1 + r.incometax2 + r.incometax3 +  r.incometax4 \
                    + r.finanExp1 + r.finanExp2 + r.finanExp3 + r.finanExp4)/(r.THEquity\
                    - r.goodwill - r.iAssets)
                # print(ROI)
                r_tuple = (r.code,ebitev,ROI,r.name)
                data_list.append(r_tuple)
    return data_list

if __name__ == '__main__':
    '''以下是测试代码'''
    # db.drop_all() #删除所有表
    # db.create_all() #新建所有表
    # getToday()
    # BasicModel('basic.xls',u'selResult').insert()
    # BasicModel('today.xls',u'Sheet1').updateToday()
    # TodayModel('today.xls',u'Sheet1').insert()
    # record = BasicTable.query.filter_by(code = '000625').first()
    d = getMFData()
    sortRoi = []
    sortEvebit = []
    sortStock = []

    d = sorted(d, key=lambda d: d[1])
    d.reverse()
#    print(d)
    #按照ROI进行排序

    for num in range(len(d)):
        sortRoi.append([d[num][0],num+1,d[num][3]])

    sortRoi = sorted(sortRoi, key=lambda sortRoi: sortRoi[0])
    #按股票代码排序
#    print(sortRoi)
    #给出每个股票的ROI排行

    d = sorted(d, key=lambda d: d[2])
    d.reverse()
    #ebitev进行排序

    for num in range(len(d)):
        sortEvebit.append([d[num][0],num+1])

    sortEvebit = sorted(sortEvebit, key=lambda sortEvebit: sortEvebit[0])
    #按股票代码排序
#    print(sortEvebit)
    #给出每个股票的ebitev排行

    for num in range(len(d)):
        sortStock.append([sortRoi[num][0],sortRoi[num][1]+sortEvebit[num][1],sortRoi[num][2]])
#    print(sortStock)

    sortStock = sorted(sortStock, key=lambda sortStock: sortStock[1])
#    print(sortStock)

    for i in range(30):
        print ("排名第%(num)s 的股票是 %(stock)s，%(name)s" % {'num':i+1,"stock":sortStock[i][0],"name":sortStock[i][2]})



'''
ebitev = (income1 + income2 + income3 + income4 + incometax1 + incometax2 + incometax3 +  incometax4 + finanExp1 +/
    finanExp2 + finanExp3 + finanExp4)/mktcap

ROI = (income1 + income2 + income3 + income4 + incometax1 + incometax2 + incometax3 +  incometax4 + finanExp1 +/
    finanExp2 + finanExp3 + finanExp4)/(THEquity- goodwill - iAssets)
'''

'''
d = [('000001', 0.7,3), ('000002',0.2, 2), ('000003',0.3, 3), ('000004',0.6, 4)]
sortRoi = []
sortEvebit = []
sortStock = []

d = sorted(d, key=lambda d: d[1])
d.reverse()
print(d)
#按照ROI进行排序

for num in range(len(d)):
    sortRoi.append([d[num][0],num+1])
sortRoi = sorted(sortRoi, key=lambda sortRoi: sortRoi[0])
#按股票代码排序
print(sortRoi)
#给出每个股票的ROI排行

d = sorted(d, key=lambda d: d[2])
d.reverse()
#ebitev进行排序

for num in range(len(d)):
    sortEvebit.append([d[num][0],num+1])
sortEvebit = sorted(sortEvebit, key=lambda sortEvebit: sortEvebit[0])
#按股票代码排序
print(sortEvebit)
#给出每个股票的ebitev排行

for num in range(len(d)):
    sortStock.append([sortRoi[num][0],sortRoi[num][1]+sortEvebit[num][1]])
print(sortStock)

sortStock = sorted(sortStock, key=lambda sortStock: sortStock[1])
print(sortStock)

for i in range(4):
    print("排名第%(num)s 的股票是 %(stock)s" % {'num':i+1,"stock":sortStock[i][0]})

def getMFData():
    #获取神奇公式计算结果
    result = BasicTable.query.all()
    data_list = []
    for record in result:
        if record.mktcap is not None:
            r_dict = {'income1':record.income1,'income2':record.income2,'income3':record.income3,'income4':record.income4,
                 'incometax1':record.incometax1,'incometax2':record.incometax2,'incometax3':record.incometax3,'incometax4':record.incometax4,
                 'finanExp1':record.finanExp1,'finanExp2':record.finanExp2,'finanExp3':record.finanExp3,'finanExp4':record.finanExp4,
                 'THEquity':record.THEquity,'iAssets':record.iAssets,'goodwill':record.goodwill,'totals':record.totals,'mktcap':record.mktcap}
            # print(record.code,r_dict)
            ebitev = (r.income1'] + r.income2'] + r.income3'] + r.income4'] \
                    + r.incometax1'] + r.incometax2'] + r.incometax3'] +  r.incometax4'] \
                    + r.finanExp1'] + r.finanExp2'] + r.finanExp3'] + r.finanExp4'])/r.mktcap']
            # print(ebitev)
            if record.THEquity != 0:
                ROI = (r.income1'] + r.income2'] + r.income3'] + r.income4']\
                    + r.incometax1'] + r.incometax2'] + r.incometax3'] +  r.incometax4'] \
                    + r.finanExp1'] + r.finanExp2'] + r.finanExp3'] + r.finanExp4'])/(r.THEquity']\
                    - r.goodwill'] - r.iAssets'])
                # print(ROI)
                r_tuple = (record.code,ebitev,ROI)
                data_list.append(r_tuple)
    return data_list
'''
