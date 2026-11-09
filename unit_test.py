from mstarpy import Stock


from mstarpy.search import MorningstarSession

session = MorningstarSession()

stock = Stock(
        "US8334451098",
        language="en-gb",
        filters={"exchange": "XNYS"},
        session=session,
    )
stock.financialSummary()