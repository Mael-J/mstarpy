from mstarpy.search import search_funds, search_filter,filter_universe, search_stock, token_investment_strategy, token_chart, token_fund_information



def test_filter_universe_with_one_term():
    filter_values = filter_universe("IndustryId")
    assert len(filter_values["IndustryId"]) > 0
    assert "name" in filter_values["IndustryId"][0]
    assert "id" in filter_values["IndustryId"][0]
    assert "sectorId" in filter_values["IndustryId"][0]
    filter_values = filter_universe("CategoryId")
    assert len(filter_values["CategoryId"]) > 0
    assert "name" in filter_values["CategoryId"][0]
    assert "id" in filter_values["CategoryId"][0]

def test_filter_universe_with_one_list_term():
    filter_values = filter_universe(["starRating"])
    assert filter_values["starRating"] == ['1', '2', '3', '4', '5']

def test_filter_universe_with_mutiple_terms():
    fields = ["SectorId", "debtEquityRatio"]
    filter_values = filter_universe(fields)
    assert len(set(filter_values.keys()) - set(fields)) == 0
    fields = ['LargestRegion','SustainabilityRank']
    filter_values = filter_universe(fields)
    assert len(set(filter_values.keys()) - set(fields)) == 0

def test_search_funds_with_fields():
    result = search_funds("F0GBR054PU", ["Universe", 'ExchangeId'])
    assert "Universe" in result[0]


def test_search_funds_with_filter():
    filters={"starRating" : (">", 2)}
    funds_list = search_funds("myria",["Name", "starRating"], filters=filters)
    assert len(funds_list) > 0
    assert "Name" in funds_list[0]
    assert "starRating" in funds_list[0]

# print(search_filter("CategoryId"))
def test_search_filters():
    filter_options = search_filter(asset_type="stock")
    assert len(filter_options) > 0
    assert "GBRReturnM12" in filter_options 
    assert "PBRatio" in filter_options 
    assert "PERatio" in filter_options 
    assert "PSRatio" in filter_options 

def test_search_stock():
    stock_list = search_stock('FR0014003J32','LegalName',exchange="PARIS")
    assert stock_list[0]["LegalName"] == "NamR SA Ordinary Shares"

def test_search_stock_with_fields():
    stock_list = search_stock(
        "a",
        field=["Name", "GBRReturnM12", "PERatio"],
        exchange='HONG-KONG'
    )
    assert len(stock_list) > 0
    assert "Name" in stock_list[0]
    assert "GBRReturnM12" in stock_list[0]
    assert "PERatio" in stock_list[0]

def test_search_stock_with_fields_and_filter():
    response = search_stock(
        term='',
        field=["Name", "fundShareClassId", "GBRReturnM12", "PERatio"], 
        exchange='PARIS', filters={
            "PERatio" : ("<", '10'),
            "GBRReturnM12" : (">", 20), 
            "debtEquityRatio" : (0, 5),
            "SectorId" : ["IG000BA008", "IG000BA006"] }
    )
    assert len(response) > 0
    assert "Name" in response[0]
    assert "fundShareClassId" in response[0]
    assert "GBRReturnM12" in response[0]
    assert "PERatio" in response[0]

def test_search_stock_with_page_size():
    stock = search_stock(
        '',
        ['SecId','TenforeId','LegalName'],
        exchange="PARIS",
        pageSize=10, 
        currency="EUR",
        filters={"GBRReturnM12":(0,20)}
    )
    assert len(stock) > 0
    assert "SecId" in stock[0]
    assert "LegalName" in stock[0]


