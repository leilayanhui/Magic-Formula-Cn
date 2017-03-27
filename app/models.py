# app/models.py

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '%d, %s, %s' % (self.id, self.username, self.password_hash)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

def magsort():
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

    return sortStock
