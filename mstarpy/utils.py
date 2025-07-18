import random

APIKEY = "lstzFDEOhfFNMLikKa0am9mgEKLBl49T"

ASSET_TYPE = ["etf", "fund", "stock"]

EXCHANGE = {
    'ARCX': 'NYSE Arca (Pacific Stock Exchange)',
    'BATS': 'BATS Exchange inc',
    'CHIA': 'Chi-X Australia',
    'E0WWE$$ALL': 'WORLDWIDE_EQUITY',
    'FINR': 'OTC Composite',
    'IPSX': 'equity_exchange_IPSX',
    'IXUS': "Standard + Poor's Indices",
    'MABX': 'Madrid stock exchange Equities',
    'MSCO': 'MSCI (EOD Only)',
    'MSTARFund': 'Morningstar Fund',
    'OTCM': 'OTC Markets (was Pinksheets)',
    'USCO': 'US composite market',
    'XAMS': 'NYSE Euronext Amsterdam Equities',
    'XASE': 'American Stock Exchange',
    'XASX': 'Australia Stock Exchange',
    'XATH': 'Athens Stock Exchange',
    'XBER': 'Berlin',
    'XBKK': 'Thailand Stock Exchange',
    'XBOM': 'Mumbai Stock Exchange',
    'XBRU': 'NYSE Euronext Brussels Equities',
    'XCNQ': 'CNSX (Canada National Stock Exchange)',
    'XCSE': 'OMX exchange Copenhagen',
    'XDUB': 'Irish Stock Exchange',
    'XDUS': 'Düsseldorf',
    'XETR': 'XETRA Frankfurt',
    'XEUR': 'EUREX (was DTB Deutsche Termin Börse)',
    'XFRA': 'Frankfurter Börse (or Germany in general)',
    'XHAM': 'Hamburg',
    'XHAN': 'Hannover (via CEF)',
    'XHEL': 'Helsinki (Equities)',
    'XHKF': 'Hong Kong Stock Exchange / Hong Kong Futures Exchange / Hang Seng Indices',
    'XHKG': 'HONG_KONG',
    'XICE': 'OMX Exchange Iceland',
    'XIST': 'Istanbul Stock Exchange',
    'XKOS': 'Korea Stock Exchange (KOSCOM)',
    'XLIS': 'NYSE Euronext Lisbon',
    'XLIT': 'OMX Exchange Vilnius',
    'XLON': 'LSE (SEAQ national)',
    'XLUX': 'Luxembourg Stock Exchange',
    'XMEX': 'Bolsa de valores Mexico',
    'XMIL': 'Milan Stock Exchange (Borsa Italia)',
    'XMUN': 'Munchen',
    'XNAS': 'NASDAQ national market',
    'XNSE': 'India National Stock Exchange',
    'XNYS': 'New York Stock Exchange',
    'XNZE': 'New Zealand Stock Exchange',
    'XOSE': 'Osaka',
    'XOSL': 'Oslo bors',
    'XOTC': 'OTCBB, over the counter bulletin board equities',
    'XPAR': 'NYSE Euronext Paris Equities',
    'XRIS': 'OMX Exchange Riga',
    'XSES': 'Singapore Stock Exchange',
    'XSHE': 'Shenzhen Stock Exchange',
    'XSHG': 'Shanghai Stock Exchange',
    'XSTO': 'NASDAQ OMX Stockholm',
    'XSTU': 'Stuttgart',
    'XSWX': 'SIX Feed (was SWX)',
    'XTAI': 'Taiwan Stock Exchange',
    'XTAL': 'Tallin Stock Exchange',
    'XTKS': 'Tokyo Stock Exchange',
    'XTSE': 'Toronto Stock Exchange',
    'XWAR': 'Warsaw Stock Exchange',
    'XWBO': 'Wiener Boerse',


}


FILTER_TYPE = [
        'basics',
        'dividends',
        'fees-and-expenses',
        'keyword',
        'other',
        'performance',
        'profitability-and-growth',
        'purchase-requirements',
        'ratings',
        'risk',
        'valuation',
 ]

LANGUAGE = {'en-ea': 'Asia',
            'nl': 'Benelux',
            'en-ca': 'CanadaEnglish',
            'fr-ca': 'CanadaFrench',
            'en-eu': 'CentralEurope',
            'fr': 'France',
            'de': 'Germany',
            'it': 'Italy',
            'ja': 'Japan',
            'en-nd': 'Nordics',
            'es': 'Spain',
            'sv': 'Sweden',
            'en-gb': 'UnitedKingdom'}

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3) Gecko/20090305 Firefox/3.1b3 GTB5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; ko; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2",
    "Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:1.9b5) Gecko/2008032620 Firefox/3.0b5",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.12) Gecko/20080214 Firefox/2.0.0.12",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8",
    "Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.0.5) Gecko/20060819 Firefox/1.5.0.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3",
    "Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7.9) Gecko/20050711 Firefox/1.0.6",
    "Mozilla/5.0 (Windows; Windows NT 6.1; rv:2.0b2) Gecko/20100720 Firefox/4.0b2",
    "Mozilla/5.0 (X11; Linux x86_64; rv:2.0b4) Gecko/20100818 Firefox/4.0b4",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20101111 Firefox/4.0b7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b8pre) Gecko/20101114 Firefox/4.0b8pre",
    "Mozilla/5.0 (X11; Linux x86_64; rv:2.0b9pre) Gecko/20110111 Firefox/4.0b9pre",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b9pre) Gecko/20101228 Firefox/4.0b9pre",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre",
    "Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2",
    "Mozilla/5.0 (X11; Linux i686 on x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2",
    "Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0",
    "Mozilla/5.0 (X11; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.36 Safari/525.19",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.3 Safari/532.2",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.201.1 Safari/532.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.173.1 Safari/530.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.558.0 Safari/534.10",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.600.0 Safari/534.14",
    "Mozilla/5.0 (X11; U; Windows NT 6; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.792.0 Safari/535.1",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
]


def random_user_agent() -> str:
    """
    This function selects a random User-Agent from the User-Agent list, . User-Agents are used in
    order to avoid the limitations of the requests to morningstar.com. The User-Agent is
    specified on the headers of the requests and is different for every request.



    Returns:
       :obj:`str` - user_agent:
            The returned:obj:`str` is the name of a random User-Agent, which will be passed on the
            headers of a request so to avoid restrictions due to the use of multiple requests from the
            same User-Agent.

    """

    return random.choice(USER_AGENTS)
