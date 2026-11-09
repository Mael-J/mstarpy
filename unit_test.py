from mstarpy import Stock


from mstarpy.search import MorningstarSession

session = MorningstarSession()

stock = Stock(
        "US0378331005",
        language="en-gb",
        filters={"exchange": "XNYS"},
        session=session,
    )
print(stock.balanceSheet())