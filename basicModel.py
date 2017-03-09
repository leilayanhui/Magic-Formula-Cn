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

# --------basicModels.py文件分割线--------
from datetime import datetime,date,timedelta
from fetchAPIData import BasicData,CycleData

class BasicTable(db.Model):
    __tablename__ = 'basicTable'
    id = db.Column(db.Integer, primary_key = True)
    lastTime = db.Column(db.DateTime,index=True,default=datetime.utcnow) #更新时间
    code = db.Column(db.String(64)) #代码
    name = db.Column(db.String(64)) #名称
    industry = db.Column(db.String(64)) #所属行业
    area = db.Column(db.String(64)) #地区
    pe = db.Column(db.Integer) #市盈率
    outstanding = db.Column(db.Integer) #流通股本(亿)
    totals = db.Column(db.Integer) #总股本(亿)
    totalAssets = db.Column(db.Integer) #总资产(万)
    liquidAssets = db.Column(db.Integer) #流动资产
    fixedAssets = db.Column(db.Integer) #固定资产
    reserved = db.Column(db.Integer) #公积金
    reservedPerShare = db.Column(db.Integer) #每股公积金
    esp = db.Column(db.Integer) #每股收益
    bvps = db.Column(db.Integer) #每股净资
    pb = db.Column(db.Integer) #市净率
    timeToMarket = db.Column(db.Integer) #上市日期
    undp = db.Column(db.Integer) #未分利润
    perundp = db.Column(db.Integer) #每股未分配
    rev = db.Column(db.Integer) #收入同比(%)
    profit = db.Column(db.Integer) #利润同比(%)
    gpr = db.Column(db.Integer) #毛利率(%)
    npr = db.Column(db.Integer) #净利润率(%)
    holders = db.Column(db.Integer) #股东人数

    def __repr__(self):
        return '<basicTable %r>' % self.name

class CycleTable(db.Model):
    __tabelname = 'cycleTable'
    id = db.Column(db.Integer, primary_key = True)
    lastTime = db.Column(db.DateTime,index=True,default=datetime.utcnow) #更新时间
    yearQuarter = db.Column(db.String(64)) #季报代码 例2014年3季报，yearQuarter = '20143'
    code = db.Column(db.String(64)) #代码
    name = db.Column(db.String(64)) #名称
    eps = db.Column(db.String(64)) #每股收益
    eps_yoy = db.Column(db.String(64)) #每股收益同比(%)
    bvps = db.Column(db.String(64)) #每股净资产
    roe = db.Column(db.String(64)) #净资产收益率(%)
    epcf = db.Column(db.String(64)) #每股现金流量(元)
    net_profits = db.Column(db.String(64)) #净利润(万元)
    profits_yoy = db.Column(db.String(64)) #净利润同比(%)
    distrib = db.Column(db.String(64)) #分配方案
    report_date = db.Column(db.String(64)) #发布日期

    net_profit_ratio = db.Column(db.String(64)) #净利率(%)
    gross_profit_rate = db.Column(db.String(64)) #毛利率(%)
    business_income = db.Column(db.String(64)) #营业收入(百万元)
    bips = db.Column(db.String(64)) #每股主营业务收入(元)

    arturnover = db.Column(db.String(64)) #应收账款周转率(次)
    arturndays = db.Column(db.String(64)) #应收账款周转天数(天)
    inventory_turnover = db.Column(db.String(64)) #存货周转率(次)
    inventory_days = db.Column(db.String(64)) #存货周转天数(天)
    currentasset_turnover = db.Column(db.String(64)) #流动资产周转率(次)
    currentasset_days = db.Column(db.String(64)) #流动资产周转天数(天)

    mbrg  = db.Column(db.String(64)) #主营业务收入增长率(%)
    nprg  = db.Column(db.String(64)) #净利润增长率(%)
    nav  = db.Column(db.String(64)) #净资产增长率
    targ  = db.Column(db.String(64)) #总资产增长率
    epsg = db.Column(db.String(64)) #每股收益增长率
    seg  = db.Column(db.String(64)) #股东权益增长率

    currentratio = db.Column(db.String(64)) #流动比率
    quickratio = db.Column(db.String(64)) #速动比率
    cashratio = db.Column(db.String(64)) #现金比率
    icratio = db.Column(db.String(64)) #利息支付倍数
    sheqratio = db.Column(db.String(64)) #股东权益比率
    adratio = db.Column(db.String(64)) #股东权益增长率

    cf_sales = db.Column(db.String(64)) #经营现金净流量对销售收入比率
    rateofreturn = db.Column(db.String(64)) #资产的经营现金流量回报率
    cf_nm = db.Column(db.String(64)) #经营现金净流量与净利润的比率
    cf_liabilities = db.Column(db.String(64)) #经营现金净流量对负债比率
    cashflowratio = db.Column(db.String(64)) #现金流量比率

    def __repr__(self):
        return '<cycleTable %r>' % self.name

def insertBasicTable():
    basic = BasicData().basic()
    data = BasicData().dataDict(basic)
    for k,v in data.items():
        record = BasicTable(code = k,
                            name = v['name'],
                            industry = v['industry'],
                            area = v['area'],
                            pe = int(v['pe']),
                            outstanding = int(v['outstanding']),
                            totals = int(v['totals']),
                            totalAssets = int(v['totalAssets']),
                            liquidAssets = int(v['liquidAssets']),
                            fixedAssets = int(v['fixedAssets']),
                            reserved = int(v['reserved']),
                            reservedPerShare = int(v['reservedPerShare']),
                            esp = int(v['esp']),
                            bvps = int(v['bvps']),
                            pb = int(v['pb']),
                            timeToMarket = int(v['timeToMarket']),
                            undp = int(v['undp']),
                            perundp = int(v['perundp']),
                            rev = int(v['rev']),
                            profit = int(v['profit']),
                            gpr = int(v['gpr']),
                            npr = int(v['npr']),
                            holders = int(v['holders']))
        db.session.add(record)
        db.session.commit()

class CycleModel(object):
    '''周期数据入库模块'''
    def __init__(self,year,quarter):
        self.year = year
        self.quarter = quarter
        self.insertMainTable()
        self.updateProfit()
        self.updateOperation()
        self.updateGrowth()
        self.updateDebtpaying()
        self.updateCashflow()

    def insertMainTable(self):
        data = CycleData(self.year,self.quarter).report()
        for k,v in data.items():
            # print(v)
            record = CycleTable(code = v['code'],
                                name = v['name'],
                                yearQuarter = str(self.year) + str(self.quarter),
                                eps = v['eps'],#每股收益
                                eps_yoy = v['eps_yoy'], #每股收益同比(%)
                                bvps = v['bvps'], #每股净资产
                                roe = v['roe'], #净资产收益率(%)
                                epcf = v['epcf'], #每股现金流量(元)
                                net_profits = v['net_profits'], #净利润(万元)
                                profits_yoy = v['profits_yoy'], #净利润同比(%)
                                distrib = v['distrib'], #分配方案
                                report_date = v['report_date']) #发布日期
            db.session.add(record)
            db.session.commit()

    def updateProfit(self):
        data = CycleData(self.year,self.quarter).profit()
        for k,v in data.items():
            code = v['code']
            yearQuarter = str(self.year) + str(self.quarter)
            record = CycleTable.query.filter_by(code = code).filter_by(yearQuarter = yearQuarter).first()
            if record is not None:
                record.net_profit_ratio = v['net_profit_ratio'] #净利率(%)
                record.gross_profit_rate = v['gross_profit_rate']#毛利率(%)
                record.business_income = v['business_income'] #营业收入(百万元)
                record.bips = v['bips'] #每股主营业务收入(元))
                db.session.add(record)
                db.session.commit()

    def updateOperation(self):
        data = CycleData(self.year,self.quarter).operation()
        for k,v in data.items():
            code = v['code']
            yearQuarter = str(self.year) + str(self.quarter)
            record = CycleTable.query.filter_by(code = code).filter_by(yearQuarter = yearQuarter).first()
            if record is not None:
                record.arturnover = v['arturnover'] #应收账款周转率(次)
                record.arturndays = v['arturndays'] #应收账款周转天数(天)
                record.inventory_turnover = v['inventory_turnover'] #存货周转率(次)
                record.inventory_days = v['inventory_days'] #存货周转天数(天)
                record.currentasset_turnover = v['currentasset_turnover'] #流动资产周转率(次)
                record.currentasset_days = v['currentasset_days'] #流动资产周转天数(天)
                db.session.add(record)
                db.session.commit()

    def updateGrowth(self):
        data = CycleData(self.year,self.quarter).growth()
        for k,v in data.items():
            code = v['code']
            # print(v)
            yearQuarter = str(self.year) + str(self.quarter)
            record = CycleTable.query.filter_by(code = code).filter_by(yearQuarter = yearQuarter).first()
            if record is not None:
                record.mbrg  = v['mbrg'] #主营业务收入增长率(%)
                record.nprg  = v['nprg'] #净利润增长率(%)
                record.nav  = v['nav'] #净资产增长率
                record.targ  = v['targ'] #总资产增长率
                record.epsg = v['epsg'] #每股收益增长率
                record.seg  = v['seg'] #股东权益增长率
                db.session.add(record)
                db.session.commit()

    def updateDebtpaying(self):
        data = CycleData(self.year,self.quarter).debtpaying()
        for k,v in data.items():
            code = v['code']
            # print(v)
            yearQuarter = str(self.year) + str(self.quarter)
            record = CycleTable.query.filter_by(code = code).filter_by(yearQuarter = yearQuarter).first()
            if record is not None:
                record.currentratio = v['currentratio'] #流动比率
                record.quickratio = v['quickratio'] #速动比率
                record.cashratio = v['cashratio'] #现金比率
                record.icratio =  v['icratio'] #利息支付倍数
                record.sheqratio =  v['sheqratio'] #股东权益比率
                record.adratio =  v['adratio'] #股东权益增长率
                db.session.add(record)
                db.session.commit()

    def updateCashflow(self):
        data = CycleData(self.year,self.quarter).cashflow()
        for k,v in data.items():
            code = v['code']
            # print(v)
            yearQuarter = str(self.year) + str(self.quarter)
            record = CycleTable.query.filter_by(code = code).filter_by(yearQuarter = yearQuarter).first()
            if record is not None:
                record.cf_sales = v['cf_sales'] #经营现金净流量对销售收入比率
                record.rateofreturn = v['rateofreturn'] #资产的经营现金流量回报率
                record.cf_nm = v['cf_nm'] #经营现金净流量与净利润的比率
                record.cf_liabilities = v['cf_liabilities'] #经营现金净流量对负债比率
                record.cashflowratio = v['cashflowratio'] #现金流量比率
                db.session.add(record)
                db.session.commit()

if __name__ == '__main__':
    '''以下是测试代码'''
    #db.drop_all() #删除所有表
    db.create_all() #新建所有表
    insertBasicTable()
    record = BasicTable.query.filter_by(code = '300396').first()

    CycleModel(2016,3)
    record = CycleTable.query.filter_by(code = '000159').first()
    a = record.seg
    b = record.cashflowratio
    print(a,b)


