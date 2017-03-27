# 神奇公式筛股器
适用中国市场的神奇公式

## 简介
借鉴格林布拉特的神奇公式，代入中国公司的财报数据，计算每支的投资回报率和收益率，依值排序，相加这两个排名，获得综合排名。排名越靠前的股票，其投资回报率和收益率的组合越佳。定期分批买入排名靠前的股票，持有一年左右抛出。既能获得优质低价的股票，又能节省大量选股时间。


## [网站](http://magicformulacn.herokuapp.com/)

## 数据来源
### 东方财富软件
最近四季的财报数据

**[软件下载](http://acttg.eastmoney.com/pub/web_pc_dcsy_top1_02_01_01_1)**

### tushare
[实时行情](http://tushare.org/trading.html#id4)  ts.get_today_all()

**[使用前提](http://tushare.org/index.html#id4)**


## 开发日志

`11w: 20170319-20170325`
- [11w 工作内容](https://github.com/leilayanhui/Magic-Formula-Cn/issues/27)

`10w: 20170312-20170318`

- 该换数据来源为东方财富通

  [原始数据获取方法](https://github.com/leilayanhui/Magic-Formula-Cn/issues/22)

- 调整神奇公式计算公式

  [新的神奇公式是怎样运算的？](https://github.com/leilayanhui/Magic-Formula-Cn/issues/26)

- [10w技术难点](https://github.com/leilayanhui/Magic-Formula-Cn/issues/18)

- [路演初稿](https://github.com/leilayanhui/Magic-Formula-Cn/issues/13)

`9w：20170305-201703011`

- [已部署 Heroku，免费账户有诸多限制，还有 bug](https://github.com/leilayanhui/Magic-Formula-Cn/issues/14)

- [**@fatfox_抓取 tushare 的数据代码(已拿代码，待代码上传GitHub)**](https://github.com/leilayanhui/Magic-Formula-Cn/tree/fatfox-db-tushare)

- **@蕙蕙_荐股页面批量倒入股票的代码**
暂未解决，以手动输入代替

- [**@zhangshiying_利用神奇公式官方主页，编写项目的help html 简介、使用方法(待代码上传GitHub)**]()

- [**@蕙蕙_9w技术点汇总**](https://github.com/leilayanhui/Magic-Formula-Cn/issues/8)

`8w：20170226-20170304`

- [**前端后端设计**](https://github.com/leilayanhui/Magic-Formula-Cn/issues/3)

- [**获取原始数据**](https://github.com/leilayanhui/Magic-Formula-Cn/issues/4)

- [**原始数据excel表格**](https://github.com/leilayanhui/Magic-Formula-Cn/issues/6)

- [**文件、类、函数中文注释**](https://github.com/leilayanhui/Magic-Formula-Cn/wiki/StructureClassDef)

- [**8w技术点汇总**](https://github.com/leilayanhui/Magic-Formula-Cn/issues/6)

