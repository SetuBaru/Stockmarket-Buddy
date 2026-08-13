import time
import threading

import yfinance as yf
from flask import Flask, jsonify, request
from flask_cors import CORS


# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)

# Allows your WordPress website to request the API.
CORS(app)


# ============================================================
# CACHE
# ============================================================

CACHE = {
    "data": None,
    "timestamp": 0
}

CACHE_LOCK = threading.Lock()

# How often Yahoo is queried.
CACHE_SECONDS = 60


# ============================================================
# MARKET DATA
# ============================================================

MARKETS = [

    # ========================================================
    # 🇺🇸 UNITED STATES - INDICES
    # ========================================================

    {
        "name": "S&P 500",
        "symbol": "^GSPC",
        "type": "index",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "NASDAQ Composite",
        "symbol": "^IXIC",
        "type": "index",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Dow Jones",
        "symbol": "^DJI",
        "type": "index",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Russell 2000",
        "symbol": "^RUT",
        "type": "index",
        "region": "US",
        "country": "United States"
    },


    # ========================================================
    # 🇺🇸 UNITED STATES - MAJOR COMPANIES
    # ========================================================

    {
        "name": "Apple",
        "symbol": "AAPL",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Microsoft",
        "symbol": "MSFT",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "NVIDIA",
        "symbol": "NVDA",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Amazon",
        "symbol": "AMZN",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Alphabet",
        "symbol": "GOOGL",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Meta",
        "symbol": "META",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Tesla",
        "symbol": "TSLA",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Berkshire Hathaway",
        "symbol": "BRK-B",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "JPMorgan Chase",
        "symbol": "JPM",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Visa",
        "symbol": "V",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Walmart",
        "symbol": "WMT",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Eli Lilly",
        "symbol": "LLY",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Broadcom",
        "symbol": "AVGO",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Oracle",
        "symbol": "ORCL",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Netflix",
        "symbol": "NFLX",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "AMD",
        "symbol": "AMD",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Palantir",
        "symbol": "PLTR",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Coca-Cola",
        "symbol": "KO",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "McDonald's",
        "symbol": "MCD",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },

    {
        "name": "Mastercard",
        "symbol": "MA",
        "type": "stock",
        "region": "US",
        "country": "United States"
    },


    # ========================================================
    # 🇸🇦 SAUDI ARABIA - INDICES
    # ========================================================

    {
        "name": "Tadawul All Share",
        "symbol": "^TASI.SR",
        "type": "index",
        "region": "MENA",
        "country": "Saudi Arabia"
    },


    # ========================================================
    # 🇸🇦 SAUDI ARABIA - MAJOR COMPANIES
    # ========================================================

    {
        "name": "Saudi Aramco",
        "symbol": "2222.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "Al Rajhi Bank",
        "symbol": "1120.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "Saudi National Bank",
        "symbol": "1180.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "SABIC",
        "symbol": "2010.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "Saudi Telecom",
        "symbol": "7010.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "Alinma Bank",
        "symbol": "1150.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "Riyad Bank",
        "symbol": "1010.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "Saudi Electricity",
        "symbol": "5110.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "ACWA Power",
        "symbol": "2082.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "Maaden",
        "symbol": "1211.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "Jarir Marketing",
        "symbol": "4190.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "Elm",
        "symbol": "7203.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "STC Solutions",
        "symbol": "7202.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "Savola",
        "symbol": "2050.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "Arab National Bank",
        "symbol": "1080.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },

    {
        "name": "Banque Saudi Fransi",
        "symbol": "1050.SR",
        "type": "stock",
        "region": "MENA",
        "country": "Saudi Arabia"
    },


    # ========================================================
    # 🇦🇪 UNITED ARAB EMIRATES - INDICES
    # ========================================================

    {
        "name": "DFM General Index",
        "symbol": "DFMGI.AE",
        "type": "index",
        "region": "MENA",
        "country": "United Arab Emirates"
    },


    # ========================================================
    # 🇶🇦 QATAR - INDICES
    # ========================================================

    {
        "name": "QE Index",
        "symbol": "^GNRI.QA",
        "type": "index",
        "region": "MENA",
        "country": "Qatar"
    },


    # ========================================================
    # 🇶🇦 QATAR - MAJOR COMPANIES
    # ========================================================

    {
        "name": "Qatar National Bank",
        "symbol": "QNBK.QA",
        "type": "stock",
        "region": "MENA",
        "country": "Qatar"
    },

    {
        "name": "Qatar Islamic Bank",
        "symbol": "QIBK.QA",
        "type": "stock",
        "region": "MENA",
        "country": "Qatar"
    },

    {
        "name": "Industries Qatar",
        "symbol": "IQCD.QA",
        "type": "stock",
        "region": "MENA",
        "country": "Qatar"
    },

    {
        "name": "Ooredoo Qatar",
        "symbol": "ORDS.QA",
        "type": "stock",
        "region": "MENA",
        "country": "Qatar"
    },


    # ========================================================
    # 🇰🇼 KUWAIT - MAJOR COMPANIES
    # ========================================================

    {
        "name": "National Bank of Kuwait",
        "symbol": "NBK.KW",
        "type": "stock",
        "region": "MENA",
        "country": "Kuwait"
    },

    {
        "name": "Kuwait Finance House",
        "symbol": "KFH.KW",
        "type": "stock",
        "region": "MENA",
        "country": "Kuwait"
    },

    {
        "name": "Zain",
        "symbol": "ZAIN.KW",
        "type": "stock",
        "region": "MENA",
        "country": "Kuwait"
    },


    # ========================================================
    # 🇪🇬 EGYPT - INDICES
    # ========================================================

    {
        "name": "EGX 30",
        "symbol": "^CASE30",
        "type": "index",
        "region": "MENA",
        "country": "Egypt"
    },


    # ========================================================
    # 🇪🇬 EGYPT - MAJOR COMPANIES
    # ========================================================

    {
        "name": "Commercial International Bank",
        "symbol": "COMI.CA",
        "type": "stock",
        "region": "MENA",
        "country": "Egypt"
    },

    {
        "name": "EFG Holding",
        "symbol": "HRHO.CA",
        "type": "stock",
        "region": "MENA",
        "country": "Egypt"
    },

    {
        "name": "Telecom Egypt",
        "symbol": "ETEL.CA",
        "type": "stock",
        "region": "MENA",
        "country": "Egypt"
    },

    {
        "name": "Talaat Moustafa",
        "symbol": "TMGH.CA",
        "type": "stock",
        "region": "MENA",
        "country": "Egypt"
    },

    {
        "name": "Eastern Company",
        "symbol": "EAST.CA",
        "type": "stock",
        "region": "MENA",
        "country": "Egypt"
    },


    # ========================================================
    # 🇲🇦 MOROCCO
    # ========================================================

    {
        "name": "MASI",
        "symbol": "^105765-USD-STRD",
        "type": "index",
        "region": "MENA",
        "country": "Morocco"
    },
]

# ============================================================
# FETCH ONE SYMBOL
# ============================================================

def fetch_symbol(market):

    symbol = market["symbol"]

    try:

        ticker = yf.Ticker(symbol)

        history = ticker.history(
            period="5d",
            interval="1d",
            auto_adjust=False
        )

        if history.empty:
            return None

        # Remove rows without close prices
        history = history.dropna(
            subset=["Close"]
        )

        if history.empty:
            return None

        latest = history.iloc[-1]

        price = float(latest["Close"])

        # Previous trading day
        if len(history) >= 2:

            previous_close = float(
                history.iloc[-2]["Close"]
            )

        else:

            previous_close = None

        if (
            previous_close is not None
            and previous_close != 0
        ):

            change = price - previous_close

            change_percent = (
                change / previous_close
            ) * 100

        else:

            change = None
            change_percent = None

        return {

            "name": market["name"],
            "symbol": symbol,
            "type": market["type"],
            "region": market["region"],
            "country": market["country"],

            "price": round(price, 4),

            "change": (
                round(change, 4)
                if change is not None
                else None
            ),

            "change_percent": (
                round(change_percent, 4)
                if change_percent is not None
                else None
            ),

            "open": (
                float(latest["Open"])
                if latest["Open"] is not None
                else None
            ),

            "high": (
                float(latest["High"])
                if latest["High"] is not None
                else None
            ),

            "low": (
                float(latest["Low"])
                if latest["Low"] is not None
                else None
            ),

            "volume": (
                int(latest["Volume"])
                if latest["Volume"] is not None
                else None
            ),

            "timestamp": int(
                history.index[-1].timestamp()
            )
        }

    except Exception as e:

        print(
            f"[ERROR] {symbol}: {e}"
        )

        return None


# ============================================================
# FETCH ALL MARKETS
# ============================================================

def fetch_all_markets():

    print(
        f"\nFetching {len(MARKETS)} instruments..."
    )

    results = []

    unavailable = []

    # --------------------------------------------------------
    # Fetch in batches using yfinance.download
    # --------------------------------------------------------

    symbols = [
        market["symbol"]
        for market in MARKETS
    ]

    try:

        data = yf.download(
            symbols,
            period="5d",
            interval="1d",
            group_by="ticker",
            auto_adjust=False,
            threads=True,
            progress=False
        )

    except Exception as e:

        print(
            f"Batch download failed: {e}"
        )

        data = None


    # --------------------------------------------------------
    # Process results
    # --------------------------------------------------------

    for market in MARKETS:

        symbol = market["symbol"]

        try:

            if data is None:
                raise ValueError(
                    "No Yahoo data"
                )

            # Multi-symbol download
            if len(symbols) > 1:

                if symbol not in data.columns.get_level_values(0):

                    raise ValueError(
                        "Symbol not returned"
                    )

                symbol_data = data[symbol]

            else:

                symbol_data = data


            symbol_data = symbol_data.dropna(
                subset=["Close"]
            )

            if symbol_data.empty:

                raise ValueError(
                    "No price data"
                )


            latest = symbol_data.iloc[-1]

            price = float(
                latest["Close"]
            )


            # Previous trading day

            if len(symbol_data) >= 2:

                previous_close = float(
                    symbol_data.iloc[-2]["Close"]
                )

            else:

                previous_close = None


            if (
                previous_close is not None
                and previous_close != 0
            ):

                change = (
                    price - previous_close
                )

                change_percent = (
                    change / previous_close
                ) * 100

            else:

                change = None
                change_percent = None


            item = {

                "name": market["name"],

                "symbol": symbol,

                "type": market["type"],

                "region": market["region"],

                "country": market["country"],

                "price": round(
                    price,
                    4
                ),

                "change": (
                    round(change, 4)
                    if change is not None
                    else None
                ),

                "change_percent": (
                    round(
                        change_percent,
                        4
                    )
                    if change_percent is not None
                    else None
                ),

                "open": safe_float(
                    latest.get("Open")
                ),

                "high": safe_float(
                    latest.get("High")
                ),

                "low": safe_float(
                    latest.get("Low")
                ),

                "volume": safe_int(
                    latest.get("Volume")
                ),

                "timestamp": int(
                    symbol_data.index[-1].timestamp()
                )
            }


            results.append(item)

            print(
                f"[OK] "
                f"{market['country']:20} "
                f"{market['name']:30} "
                f"{price}"
            )


        except Exception as e:

            unavailable.append({

                "name": market["name"],

                "symbol": symbol,

                "country": market["country"],

                "error": str(e)

            })

            print(
                f"[NO DATA] "
                f"{market['country']:20} "
                f"{market['name']:30} "
                f"{symbol}"
            )


    print(
        f"\nSuccessfully fetched: "
        f"{len(results)}"
    )

    print(
        f"Unavailable: "
        f"{len(unavailable)}"
    )


    return results, unavailable


# ============================================================
# SAFE CONVERSION
# ============================================================

def safe_float(value):

    try:

        if value is None:
            return None

        return float(value)

    except Exception:

        return None


def safe_int(value):

    try:

        if value is None:
            return None

        return int(value)

    except Exception:

        return None


# ============================================================
# GET CACHED DATA
# ============================================================

def get_market_data():

    now = time.time()

    with CACHE_LOCK:

        if (
            CACHE["data"] is not None
            and (
                now - CACHE["timestamp"]
            ) < CACHE_SECONDS
        ):

            print(
                "Returning cached data"
            )

            return CACHE["data"]


    # --------------------------------------------------------
    # Fetch fresh data
    # --------------------------------------------------------

    results, unavailable = (
        fetch_all_markets()
    )


    response = {

        "success": True,

        "count": len(results),

        "timestamp": int(
            time.time()
        ),

        "cache_seconds": CACHE_SECONDS,

        "data": results,

        "unavailable": unavailable

    }


    with CACHE_LOCK:

        CACHE["data"] = response

        CACHE["timestamp"] = now


    return response


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def index():

    return jsonify({

        "status": "ok",

        "service": "MENA + US Market Data API",

        "endpoint": "/market-data",

        "instruments": len(MARKETS),

        "cache_seconds": CACHE_SECONDS

    })


@app.route("/market-data")
def market_data():

    data = get_market_data()

    return jsonify(data)


# ============================================================
# FILTERED DATA
# ============================================================

@app.route("/market-data/<region>")
def market_region(region):

    data = get_market_data()

    region = region.upper()

    filtered = [

        item
        for item in data["data"]

        if item["region"].upper() == region

    ]

    return jsonify({

        "success": True,

        "region": region,

        "count": len(filtered),

        "timestamp": data["timestamp"],

        "data": filtered

    })


# ============================================================
# COUNTRY FILTER
# ============================================================

@app.route("/market-data/country/<country>")
def market_country(country):

    data = get_market_data()

    country_lower = country.lower()

    filtered = [

        item
        for item in data["data"]

        if item["country"].lower()
        == country_lower

    ]

    return jsonify({

        "success": True,

        "country": country,

        "count": len(filtered),

        "timestamp": data["timestamp"],

        "data": filtered

    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("MENA + US MARKET DATA API")
    print("=" * 70)

    print(
        f"Instruments configured: "
        f"{len(MARKETS)}"
    )

    print(
        "Cache:",
        CACHE_SECONDS,
        "seconds"
    )

    print(
        "Server: http://0.0.0.0:8005"
    )

    print("=" * 70)
    print()

    app.run(
        host="0.0.0.0",
        port=8005,
        debug=False
    )