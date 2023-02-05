from mstarpy import Funds, search_field
import datetime
import pandas as pd

start_date = datetime.datetime.today() - datetime.timedelta(90)
end_date = datetime.datetime.today()

data = Funds("vfiax", 'us').nav(start_date, end_date,'monthly')

print(pd.DataFrame(data))








