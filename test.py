from mstarpy import Funds, search_field, Stock

from mstarpy.security import Security
import datetime
import pandas as pd
from mstarpy.search import search_funds, search_filter,filter_universe, search_stock, token_investment_strategy, token_chart, token_fund_information
from mstarpy.utils import FILTER_FUND, FILTER_STOCK, EXCHANGE


    
code = "FOUSA00LIX"
fund = Funds(code,country="us")
print(fund.name)

print(fund.carbonMetrics())
start_date = datetime.date(2018,1,1)
end_date = datetime.date.today()
history = fund.nav(start_date,end_date)
print(history)

#print(Funds("myria").investmentLookup())
# print(list(EXCHANGE))
# #print(search_stock("a",field=["Name", "fundShareClassId", "GBRReturnM12", "PERatio"], exchange='HONG-KONG'))
# ms = Stock("MSFT", exchange="NASDAQ")

# top_owner = ms.mutualFundConcentratedOwners(top = 100)
# df = pd.DataFrame(top_owner["rows"])
# print(df)
# df.to_excel('test.xlsx', index = False)

# filter_value = filter_universe(["starRating"])
# print(filter_value)
#filters={"starRating" : (">", 2)}
# print(search_funds("myria",["Name","starRating"],filters={"starRating" : (">",2)}))

#print(search_filter(asset_type="stock"))
#print(filter_universe(["SectorId", "debtEquityRatio"]))


# response = search_stock(term='',field=["Name", "fundShareClassId", "GBRReturnM12", "PERatio"], 
#                          exchange='PARIS', filters={"PERatio" : ("<", '10'), "GBRReturnM12" : (">", 20), 
#                                                     "debtEquityRatio" : (0, 5), "SectorId" : ["IG000BA008", "IG000BA006"] })
# df = pd.DataFrame(response)

# print(df.head())

#print(FILTER)
#print('AdministratorCompanyId' in FILTER)

# start_date = datetime.datetime(2013,1,1)
# end_date = datetime.datetime.today()

#print(filter_universe('IndustryId'))
#print(search_stock('FR0014003J32','LegalName',exchange="PARIS"))

#print(search_stock('',['SecId','TenforeId','LegalName'], exchange="PARIS", pageSize=10,currency="EUR",filters={"GBRReturnM12":(0,20)}))

# security = Security("visa",exchange='NYSE')
# print(security)
# print(security.name)
# code = security.code
# print(search_funds(code,["Universe", 'ExchangeId']))
# print(security.asset_type)
# print(search_filter("CategoryId"))
# print(filter_universe("CategoryId"))

# print(filter_universe(['StarRatingM2556', 'LargestRegion','SustainabilityRank' ],proxies=proxies))

# stock = Stock("360 DigiTech Inc")

# print(stock.name)
# print(stock.asset_type)
# print(stock.isin)

# print(stock.analysisData())
# print(stock.analysisReport())
# print(stock.balanceSheet('annual', 'original'))
# print(stock.boardOfDirectors())
# print(stock.cashFlow('annual', 'restated'))
# print(stock.dividends())
# print(stock.esgRisk())
# print(stock.financialHealth())
# print(stock.financialSummary('quarterly', 'original'))
# print(stock.freeCashFlow())
# print(stock.incomeStatement('annual', 'original'))
# print(stock.institutionBuyers(top=5))
# print(stock.institutionConcentratedOwners(top=10))
# print(stock.institutionOwnership())
# print(stock.institutionSellers(top=5))
# print(stock.historical(start_date=start_date, end_date=end_date))
# print(stock.keyExecutives())
# print(stock.keyRatio())
# print(stock.mutualFundBuyers(top=5))
# print(stock.mutualFundConcentratedOwners(top=10))
# print(stock.mutualFundOwnership())
# print(stock.mutualFundSellers(top=5))
# print(stock.operatingGrowth())
#print(stock.operatingMargin())
# print(stock.operatingPerformance())
# print(stock.split())
# print(stock.trailingTotalReturn())
# print(stock.transactionHistory())
# print(stock.transactionSummary())
# print(stock.valuation())







# funds = Funds("LU1085283973")
# print(funds.code)
# print(funds.isin)
# print(funds.name)

# print(funds.asset_type)
# print(funds.allocationMap())
# print(funds.dataPoint("TenforeId"))
# print(funds.allocationWeighting())
# print(funds.analystRating())
# print(funds.analystRatingTopFunds())
# print(funds.analystRatingTopFundsUpDown())
# #print(funds.benchmark())
# print(funds.carbonMetrics())
# #print(funds.category())
# #print(funds.categoryAnnualPerformance())
# #print(funds.categoryCumulativePerformance())
# #print(funds.contact())
# print(funds.costIllustration())
# print(funds.couponRange())
# print(funds.creditQuality())
# print(funds.dataPoint([    'FeeLevel',
#     'fundshareClassId',
#     'fundsize',
#     'fundstyle',]))
# print(funds.distribution())
# print(funds.equityStyle())
# print(funds.equityStyleBoxHistory())
# print(funds.esgData())
# #print(funds.factorProfile())
# print(funds.feeLevel())
# #print(funds.fees())
# print(funds.financialMetrics())
# print(funds.fixedIncomeStyle())
# print(funds.fixedincomeStyleBoxHistory())
# #print(funds.fundsAnnualPerformance())
# #print(funds.fundsAnnualRank())
# #print(funds.fundsCumulativePerformance())
# #print(funds.fundsQuarterlyPerformance())
# print(funds.graphData())
#print(funds.historicalData())
# #print(funds.historicalExpenses())
# print(funds.holdings())
#print(funds.indexAnnualPerformance())
#print(funds.indexCumulativePerformance())
#print(funds.investmentStrategy())
# print(funds.marketCapitalization())
# print(funds.maturitySchedule())
# print(funds.maxDrawDown())
# print(funds.morningstarAnalyst())
# print(funds.multiLevelFixedIncomeData())
# df = pd.DataFrame(funds.nav(start_date = start_date, end_date=end_date))
# print(df)
# #print(funds.objectiveInvestment())
# print(funds.otherFee())
# print(funds.ownershipZone())
# print(funds.parentMstarRating())
# print(funds.parentSummary())
# print(funds.people())
# print(funds.position())
# print(funds.productInvolvement())
# print(funds.proxyVotingManagement())
# print(funds.proxyVotingShareHolder())
# #print(funds.referenceIndex('category'))
# print(funds.regionalSector())
# print(funds.regionalSectorIncludeCountries())
# print(funds.riskReturnScatterplot())
# print(funds.riskReturnSummary())
# print(funds.riskVolatility())
# print(funds.salesFees())
# print(funds.sector())
# print(funds.starRatingFundAsc())
# print(funds.starRatingFundDesc())
# print(funds.taxes())
# print(funds.trailingReturn())










