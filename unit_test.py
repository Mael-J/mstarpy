from mstarpy import Stock, Funds
from mstarpy.search import MorningstarSession
import datetime

session = MorningstarSession()

end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(days=30)

# stock = Stock(
#         "US0378331005",
#         language="en-gb",
#         filters={"exchange": "XNYS"},
#         session=session,
#     )
# print(stock.balanceSheet())

fund = Funds("VTSAX", session=session)

print(fund.nav(start_date, end_date))