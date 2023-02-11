from mstarpy import Funds, search_field
import datetime
import pandas as pd
from mstarpy.search import search_funds, search_filter,filter_universe
from mstarpy.utils import FILTER

#print(FILTER)
#print('AdministratorCompanyId' in FILTER)

start_date = datetime.datetime(2021,1,1)
end_date = datetime.datetime.today()

etf = Funds("myria")


print(etf.isin)
print(etf.asset_type)
print(etf.allocationMap())
print(etf.allocationWeighting())
print(etf.analystRating())
print(etf.analystRatingTopFunds())
print(etf.analystRatingTopFundsUpDown())
#print(etf.benchmark())
print(etf.carbonMetrics())
#print(etf.category())
#print(etf.categoryAnnualPerformance())
#print(etf.categoryCumulativePerformance())
#print(etf.contact())
print(etf.costIllustration())
print(etf.couponRange())
print(etf.creditQuality())
print(etf.dataPoint([    'FeeLevel',
    'etfhareClassId',
    'etfize',
    'etftyle',]))
print(etf.distribution())
print(etf.equityStyle())
print(etf.equityStyleBoxHistory())
print(etf.esgData())
print(etf.factorProfile())
print(etf.feeLevel())
#print(etf.fees())
print(etf.financialMetrics())
print(etf.fixedIncomeStyle())
print(etf.fixedincomeStyleBoxHistory())
#print(etf.etfAnnualPerformance())
#print(etf.etfAnnualRank())
#print(etf.etfCumulativePerformance())
#print(etf.etfQuarterlyPerformance())
print(etf.graphData())
print(etf.historicalData())
print(etf.historicalExpenses())
print(etf.holdings())
#print(etf.indexAnnualPerformance())
#print(etf.indexCumulativePerformance())
print(etf.marketCapitalization())
print(etf.maturitySchedule())
print(etf.maxDrawDown())
print(etf.morningstarAnalyst())
print(etf.multiLevelFixedIncomeData())
print(etf.nav(start_date = start_date, end_date=end_date))
#print(etf.objectiveInvestment())
print(etf.otherFee())
print(etf.ownershipZone())
print(etf.parentMstarRating())
print(etf.parentSummary())
print(etf.people())
print(etf.position())
print(etf.productInvolvement())
print(etf.proxyVotingManagement())
print(etf.proxyVotingShareHolder())
#print(etf.referenceIndex('category'))
print(etf.regionalSector())
print(etf.regionalSectorIncludeCountries())
print(etf.riskReturnScatterplot())
print(etf.riskReturnSummary())
print(etf.riskVolatility())
print(etf.salesFees())
print(etf.sector())
print(etf.starRatingFundAsc())
print(etf.starRatingFundDesc())
print(etf.taxes())
print(etf.trailingReturn())










