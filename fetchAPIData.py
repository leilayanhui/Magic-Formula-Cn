# -*- conding: utf-8 -*-

import json
import tushare as ts # tushare数据库

class BasicData(object):
	'''基础数据'''
	def __init__(self):
		self.basic()

	def basic(self):
		'''
		获取基础数据,json格式:
		code,代码
		name,名称
		industry,所属行业
		area,地区
		pe,市盈率
		outstanding,流通股本(亿)
		totals,总股本(亿)
		totalAssets,总资产(万)
		liquidAssets,流动资产
		fixedAssets,固定资产
		reserved,公积金
		reservedPerShare,每股公积金
		esp,每股收益
		bvps,每股净资
		pb,市净率
		timeToMarket,上市日期
		undp,未分利润
		perundp, 每股未分配
		rev,收入同比(%)
		profit,利润同比(%)
		gpr,毛利率(%)
		npr,净利润率(%)
		holders,股东人数
		'''
		data = ts.get_stock_basics()
		# data.to_json('basic.json',orient='index')
		return data

	def dataDict(self,data):
		'''直接获取json数据'''
		data = data.to_json(orient='index')
		dict = json.loads(data)
		return dict

	def jsonDict(self,jsonFile):
		'''通过json文件获取数据'''
		data = data.to_json(jsonFile,orient='index')
		with open(jsonFile,'r',encoding='utf-8') as f:
			data = f.read()
		dict = json.loads(data)
		return dict

class CycleData(BasicData):
	'''周期数据'''
	def __init__(self,year,quarter):
		self.year = year
		self.quarter = quarter

	def report(self):
		'''
		获取年、季报数据,json格式：
		code,代码
		name,名称
		esp,每股收益
		eps_yoy,每股收益同比(%)
		bvps,每股净资产
		roe,净资产收益率(%)
		epcf,每股现金流量(元)
		net_profits,净利润(万元)
		profits_yoy,净利润同比(%)
		distrib,分配方案
		report_date,发布日期
		'''
		data = ts.get_report_data(self.year,self.quarter)
		dict = self.dataDict(data)
		return dict

	def profit(self):
		'''
		获取年、季盈利能力数据,json格式：
		code,代码
		name,名称
		roe,净资产收益率(%)
		net_profit_ratio,净利率(%)
		gross_profit_rate,毛利率(%)
		net_profits,净利润(万元)
		esp,每股收益
		business_income,营业收入(百万元)
		bips,每股主营业务收入(元)
		'''
		data = ts.get_profit_data(self.year,self.quarter)
		dict = self.dataDict(data)
		return dict

	def operation(self):
		'''
		按年度、季度获取营运能力数据:
		code,代码
		name,名称
		arturnover,应收账款周转率(次)
		arturndays,应收账款周转天数(天)
		inventory_turnover,存货周转率(次)
		inventory_days,存货周转天数(天)
		currentasset_turnover,流动资产周转率(次)
		currentasset_days,流动资产周转天数(天)
		'''
		data = ts.get_operation_data(self.year,self.quarter)
		dict = self.dataDict(data)
		return dict

	def growth(self):
		'''
		按年度、季度获取成长能力数据:
		code,代码
		name,名称
		mbrg,主营业务收入增长率(%)
		nprg,净利润增长率(%)
		nav,净资产增长率
		targ,总资产增长率
		epsg,每股收益增长率
		seg,股东权益增长率
		'''
		data = ts.get_growth_data(self.year,self.quarter)
		dict = self.dataDict(data)
		return dict

	def debtpaying(self):
		'''
		按年度、季度获取偿债能力数据:
		code,代码
		name,名称
		currentratio,流动比率
		quickratio,速动比率
		cashratio,现金比率
		icratio,利息支付倍数
		sheqratio,股东权益比率
		adratio,股东权益增长率
		'''
		data = ts.get_debtpaying_data(self.year,self.quarter)
		dict = self.dataDict(data)
		return dict

	def cashflow(self):
		'''
		按年度、季度获取现金流量数据:
		code,代码
		name,名称
		cf_sales,经营现金净流量对销售收入比率
		rateofreturn,资产的经营现金流量回报率
		cf_nm,经营现金净流量与净利润的比率
		cf_liabilities,经营现金净流量对负债比率
		cashflowratio,现金流量比率
		'''
		data = ts.get_cashflow_data(self.year,self.quarter)
		dict = self.dataDict(data)
		return dict

if __name__ == '__main__':
	'''引用示例,以下是测试代码'''
	dataDict = CycleData(2014,3).cashflow()

	print(type(dataDict))

	for k,v in dataDict.items():
		print(k)
		for key,value in v.items():
			print(key,value)




