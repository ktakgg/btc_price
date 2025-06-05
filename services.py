import requests
import os
# from flask import current_app # Import it later, or more carefully

# Ideally, use a more robust API and handle API keys securely (e.g., via environment variables)
# For this example, we'll use CoinGecko's public API, which doesn't require a key for basic price checks.
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

def _get_logger():
    """Safely get Flask's current_app.logger or a default print-based logger."""
    try:
        from flask import current_app
        if current_app:
            return current_app.logger
    except RuntimeError: # Working outside of application context
        pass
    except ImportError: # Flask not available
        pass
    
    # Fallback logger
    class PrintLogger:
        def error(self, msg): print(f"ERROR: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
        def info(self, msg): print(f"INFO: {msg}")
        def debug(self, msg): print(f"DEBUG: {msg}")
    return PrintLogger()

def get_crypto_price_data(crypto_symbol, target_currency):
    """
    Fetches the current price of a cryptocurrency in a specified currency.
    Example: crypto_symbol='bitcoin', target_currency='usd'
    """
    logger = _get_logger()
    symbol_to_id_map = {
        "BTC": "bitcoin", "ETH": "ethereum", "LTC": "litecoin", "XRP": "ripple",
        "BCH": "bitcoin-cash", "ADA": "cardano", "DOT": "polkadot",
        "DOGE": "dogecoin", "SOL": "solana",
    }
    crypto_id = symbol_to_id_map.get(crypto_symbol.upper(), crypto_symbol.lower())
    
    params = {'ids': crypto_id, 'vs_currencies': target_currency.lower()}

    try:
        response = requests.get(COINGECKO_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if crypto_id in data and target_currency.lower() in data[crypto_id]:
            return {"price": data[crypto_id][target_currency.lower()]}
        else:
            error_msg = f"Data not found for {crypto_symbol} in {target_currency}."
            if not data or crypto_id not in data:
                 error_msg = f"Cryptocurrency '{crypto_symbol}' (ID: {crypto_id}) not found by API."
            elif target_currency.lower() not in data.get(crypto_id, {}):
                 error_msg = f"Currency '{target_currency}' not supported for '{crypto_symbol}' by API."
            logger.warning(f"CoinGecko API did not return expected data. Symbol: {crypto_symbol}, Currency: {target_currency}. Response: {data}. Error: {error_msg}")
            return {"error": error_msg}

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error: {http_err} - Response: {getattr(http_err, 'response', None)}")
        return {"error": f"API error: Server returned status {http_err.response.status_code if http_err.response else 'N/A'}."}
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error: {conn_err}")
        return {"error": "Failed to connect to API. Check internet connection."}
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error: {timeout_err}")
        return {"error": "API request timed out."}
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error: {req_err}")
        return {"error": "Error during API request."}
    except ValueError as json_err: # Includes JSONDecodeError
        logger.error(f"JSON decode error: {json_err}")
        return {"error": "Failed to parse API response."}

if __name__ == '__main__':
    print("Testing get_crypto_price_data function (direct execution)...")
    
    # Test cases
    test_cases = [
        ('bitcoin', 'usd'),
        ('ethereum', 'eur'),
        ('BTC', 'GBP'),        # Test uppercase symbol
        ('Solana', 'USD'),     # Test mixed case symbol
        ('XYZ', 'USD'),        # Test non-existent crypto
        ('bitcoin', 'XYZ'),    # Test non-existent currency
        ('dogecoin', 'jpy'),
    ]

    for symbol, currency in test_cases:
        print(f"\nFetching price for {symbol} in {currency}...")
        result = get_crypto_price_data(symbol, currency)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Price: {result['price']}")

    print("\nTest finished.")
