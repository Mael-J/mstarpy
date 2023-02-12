from mstarpy import Funds, search_field
import datetime
import pandas as pd
from mstarpy.search import search_funds, search_filter,filter_universe
from mstarpy.utils import FILTER

#print(FILTER)
#print('AdministratorCompanyId' in FILTER)

start_date = datetime.datetime(2021,1,1)
end_date = datetime.datetime.today()


funds = Funds("myria", proxies={})

# print(filter_universe(['StarRatingM2556', 'LargestRegion','SustainabilityRank' ],proxies=proxies))

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
print(funds.historicalExpenses())
# print(funds.holdings())
# #print(funds.indexAnnualPerformance())
# #print(funds.indexCumulativePerformance())
# print(funds.investmentStrategy())
# print(funds.marketCapitalization())
# print(funds.maturitySchedule())
# print(funds.maxDrawDown())
# print(funds.morningstarAnalyst())
# print(funds.multiLevelFixedIncomeData())
# print(funds.nav(start_date = start_date, end_date=end_date))
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










