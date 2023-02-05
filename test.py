from mstarpy import Funds, search_field
import datetime
import pandas as pd
from mstarpy.search import search_funds, search_filter,filter_universe
from mstarpy.utils import FILTER

#print(FILTER)
#print('AdministratorCompanyId' in FILTER)

# funds = Funds("vfiax","us")
# print(funds.isin)
#print(search_filter())
# print(filter_universe('administratorCompanyId'))

result = search_funds('equity',['SecId','TenforeId','LegalName'], country="fr", pageSize=10,currency="EUR",filters={"GBRReturnM12":(0,5)})
print(result)
# print(len(result))








