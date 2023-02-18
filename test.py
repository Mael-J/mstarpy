from mstarpy import Funds, search_field, Stock

from mstarpy.security import Security
import datetime
import pandas as pd
from mstarpy.search import search_funds, search_filter,filter_universe, search_stock
from mstarpy.utils import FILTER_FUND, FILTER_STOCK

#print(FILTER)
#print('AdministratorCompanyId' in FILTER)

start_date = datetime.datetime(2023,1,4)
end_date = datetime.datetime.today() + datetime.timedelta(15)

#print(filter_universe('IndustryId'))
#print(search_stock('FR0014003J32','LegalName',exchange="PARIS"))

print(search_stock('',['SecId','TenforeId','LegalName'], exchange="PARIS", pageSize=10,currency="EUR",filters={"GBRReturnM12":(0,20)}))

# security = Security("visa",exchange='NYSE')
# print(security)
# print(security.name)
# code = security.code
# print(search_funds(code,["Universe", 'ExchangeId']))
# print(security.asset_type)
# print(search_filter("CategoryId"))
# print(filter_universe("CategoryId"))

# print(filter_universe(['StarRatingM2556', 'LargestRegion','SustainabilityRank' ],proxies=proxies))

# stock = Stock("US02079K3059", exchange="NASDAQ")

# print(stock.name)
# print(stock.asset_type)

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







#funds = Funds("visa", proxies={})
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
# print(funds.factorProfile())
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
# print(funds.historicalData())
# print(funds.historicalExpenses())
# print(funds.holdings())
# #print(funds.indexAnnualPerformance())
# #print(funds.indexCumulativePerformance())
# print(funds.investmentStrategy())
# print(funds.marketCapitalization())
# print(funds.maturitySchedule())
# print(funds.maxDrawDown())
# print(funds.morningstarAnalyst())
# print(funds.multiLevelFixedIncomeData())
#print(funds.nav(start_date = start_date, end_date=end_date))
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










