import yfinance as yf
from decimal import Decimal

def get_live_stock_data(ticker):
    """
    Fetches the latest closing price and basic info for a given ticker.
    For Indian stocks (NSE/BSE), the ticker usually needs a suffix like '.NS' or '.BO'.
    """
    try:
        stock = yf.Ticker(ticker)
        # Fetch just the last day to keep it fast
        hist = stock.history(period="1d")
        
        if hist.empty:
            return None
            
        # Extract the latest closing price
        current_price = Decimal(str(hist['Close'].iloc[-1]))
        info = stock.info
        
        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "company_name": info.get('shortName', ticker),
            "currency": info.get('currency', 'INR'),
            "previous_close": Decimal(str(info.get('regularMarketPreviousClose', current_price)))
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None