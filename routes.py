from flask import render_template, request, jsonify, current_app
from .services import get_crypto_price_data # Assuming services.py will handle API calls

@current_app.route('/')
def index():
    return render_template('index.html')

@current_app.route('/get_crypto_value', methods=['POST'])
def get_crypto_value():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    crypto_symbol = data.get('crypto_symbol')
    amount_owned = data.get('amount')
    target_currency = data.get('currency')

    if not crypto_symbol or not amount_owned or not target_currency:
        return jsonify({"error": "Missing data: crypto_symbol, amount, or currency"}), 400

    try:
        amount_owned = float(amount_owned)
        if amount_owned <= 0:
            raise ValueError("Amount must be positive")
    except ValueError as e:
        return jsonify({"error": f"Invalid amount: {e}"}), 400

    price_data = get_crypto_price_data(crypto_symbol, target_currency)

    if price_data.get("error"):
        return jsonify({"error": price_data["error"]}), 400 # Or a more specific error code like 502 for bad gateway if API fails

    try:
        price_per_unit = price_data['price']
        total_value = price_per_unit * amount_owned

        return jsonify({
            "symbol": crypto_symbol,
            "currency": target_currency,
            "price_per_unit": price_per_unit,
            "amount_owned": amount_owned,
            "total_value": total_value
        })
    except KeyError:
        # This might happen if the API response structure is not as expected
        return jsonify({"error": "Failed to parse price data from external API."}), 500
    except Exception as e:
        # Catch any other unexpected errors
        current_app.logger.error(f"Error processing request: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500
