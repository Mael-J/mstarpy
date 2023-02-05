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

result = search_funds("",['GBRReturnM12','TenforeId','Name', 'ReturnM12'],filters={"GBRReturnM12":(0,5),"AdministratorCompanyId" : ["0C00004AM7","0C00001OGC"] })
print(result)
# print(len(result))








