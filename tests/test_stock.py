import pytest
import datetime
from mstarpy import Funds, search_field, Stock

@pytest.fixture
def stock_history():
    stock = {
        "id": "F00000TW95",
        "ticker": "MSFT",
        "exchange": "NASDAQ",
        "start_date": datetime.date(2022,4,11),
        "end_date": datetime.date(2022,4,25),
        "history": [
            {'open': 291.79, 'high': 292.61, 'low': 285.0, 'close': 285.26, 'volume': 34569264, 'previousClose': 296.97, 'date': '2022-04-11'},
            {'open': 289.235, 'high': 290.739, 'low': 280.49, 'close': 282.06, 'volume': 30966721, 'previousClose': 285.26, 'date': '2022-04-12'},
            {'open': 282.73, 'high': 288.58, 'low': 281.3, 'close': 287.62, 'volume': 21907176, 'previousClose': 282.06, 'date': '2022-04-13'},
            {'open': 288.09, 'high': 288.305, 'low': 279.32, 'close': 279.83, 'volume': 28221607, 'previousClose': 287.62, 'date': '2022-04-14'},
            {'open': 278.91, 'high': 282.46, 'low': 278.34, 'close': 280.52, 'volume': 20778000, 'previousClose': 279.83, 'date': '2022-04-18'},
            {'open': 279.38, 'high': 286.17, 'low': 278.41, 'close': 285.3, 'volume': 22297720, 'previousClose': 280.52, 'date': '2022-04-19'},
            {'open': 289.4, 'high': 289.7, 'low': 285.3702, 'close': 286.36, 'volume': 22906667, 'previousClose': 285.3, 'date': '2022-04-20'},
            {'open': 288.58, 'high': 293.3, 'low': 280.06, 'close': 280.81, 'volume': 29454587, 'previousClose': 286.36, 'date': '2022-04-21'},
            {'open': 281.68, 'high': 283.2, 'low': 273.38, 'close': 274.03, 'volume': 29405798, 'previousClose': 280.81, 'date': '2022-04-22'},
            {'open': 273.29, 'high': 281.11, 'low': 270.77, 'close': 280.72, 'volume': 35678852, 'previousClose': 274.03, 'date': '2022-04-25'},
        ]
    }
    return stock 

def test_stock_top_owners():
    ms = Stock("MSFT", exchange="NASDAQ")
    top_owner = ms.mutualFundConcentratedOwners(top = 100)
    assert "rows" in top_owner
    assert "columnDefs" in top_owner

def test_stock_asset_type():
    stock = Stock("Tesla Inc", exchange="NASDAQ")
    assert stock.asset_type == "stock"

def test_stock_isin():
    reference = {
        "name": "Tesla Inc",
        "ticker": "TSLA",
        "exchange": "NASDAQ",
        "isin": "US88160R1014",
        "code": "0P0000OQN8"
    }
    stock = Stock(reference["name"], exchange=reference["exchange"])
    assert stock.code == reference["code"]
    assert stock.isin == reference["isin"]

def test_stock_two():
    stock = Stock("Tesla Inc", exchange="NASDAQ")
    stock.name
    stock.asset_type
    stock.isin    # ticker instead of isin
    stock.analysisData()
    stock.analysisReport()
    stock.balanceSheet('annual', 'original')
    stock.boardOfDirectors()
    stock.cashFlow('annual', 'restated')
    stock.dividends()
    stock.esgRisk()
    stock.financialHealth()
    stock.financialSummary('quarterly', 'original')
    stock.freeCashFlow()
    stock.incomeStatement('annual', 'original')
    stock.institutionBuyers(top=5)
    stock.institutionConcentratedOwners(top=10)
    stock.institutionOwnership()
    stock.institutionSellers(top=5)
    stock.keyExecutives()
    stock.keyRatio()
    stock.mutualFundBuyers(top=5)
    stock.mutualFundConcentratedOwners(top=10)
    stock.mutualFundOwnership()
    stock.mutualFundSellers(top=5)
    stock.operatingGrowth()
    stock.operatingMargin()
    stock.operatingPerformance()
    stock.split()
    stock.trailingTotalReturn()
    stock.transactionHistory()
    stock.transactionSummary()
    stock.valuation()

def test_stock_historial(stock_history):
    stock = Stock(
        stock_history["ticker"],
        exchange=stock_history["exchange"])
    history = stock.historical(
        start_date=stock_history["start_date"],
        end_date=stock_history["end_date"])
    assert history == stock_history["history"]

