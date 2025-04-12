def convert_currency(amount, currency):
    """Convert amount to the selected currency using static exchange rates."""
    exchange_rates = {
        "USD": 1,       # Base currency
        "EUR": 0.91,    # Example: 1 USD = 0.91 EUR
        "GBP": 0.78,    # Example: 1 USD = 0.78 GBP
        "NGN": 1500,    # Example: 1 USD = 1500 NGN
    }
    return round(amount * exchange_rates.get(currency, 1), 2)
