# import numpy as np
# from sklearn.linear_model import LinearRegression, LogisticRegression
# from sklearn.preprocessing import PolynomialFeatures


# # def safe_float(value):
# #     try:
# #         return float(value)
# #     except (ValueError, TypeError):
# #         return 0.0
# # --- Slippage Model ---
# def estimate_slippage(price_levels, quantity):

#     prices = np.array([float(p[0]) for p in price_levels])
#     volumes = np.array([float(p[1]) for p in price_levels])

#     cumulative_volume = np.cumsum(volumes)
#     fill_index = np.argmax(cumulative_volume >= quantity)
#     execution_price = prices[fill_index] if fill_index < len(prices) else prices[-1]
#     mid_price = (prices[0] + prices[-1]) / 2

#     slippage = abs(execution_price - mid_price) / mid_price
#     return round(slippage * 100, 4)  # In percentage

# # --- Fee Model ---
# def estimate_fee(fee_tier: str, quantity: float):
#     fee_map = {
#         'tier_1': 0.001,  # 0.1%
#         'tier_2': 0.0007, # 0.07%
#         'tier_3': 0.0005  # 0.05%
#     }
#     rate = fee_map.get(fee_tier, 0.001)
#     return round(quantity * rate, 4)

# # --- Market Impact (Almgren-Chriss Simplified) ---
# def estimate_market_impact(volatility, quantity, liquidity=1000000):
#     sigma = float(volatility)
#     q = float(quantity)
#     L = float(liquidity)

#     impact = (sigma * q) / (L + 1e-8)
#     return round(impact, 4)

# # --- Maker/Taker Proportion Model ---
# _logistic_model = LogisticRegression()
# def train_maker_taker_model():
#     # Toy training dataset
#     X = np.array([[0.01], [0.02], [0.03], [0.05], [0.08], [0.13]])  # slippage
#     y = [0, 0, 0, 1, 1, 1]  # 0 = maker, 1 = taker
#     _logistic_model.fit(X, y)

# def predict_maker_taker(slippage):
#     return float(_logistic_model.predict_proba([[slippage]])[0][1])  # taker prob

# # def estimate_slippage(data):
# #     quantity = safe_float(data.get("quantity"))

# train_maker_taker_model()

import numpy as np
from sklearn.linear_model import LogisticRegression

# --- Slippage Model ---
def estimate_slippage(price_levels, quantity):
    # BAD if you're sending strings or headers
    # price_levels = [['t', 'amount'], ['27000.1', '0.1']]

    # GOOD
    price_levels = [[27000.1, 0.1], [27000.3, 0.15], [27000.7, 0.2]]

    try:
        # Debug: show what you're receiving
        print("price_levels:", price_levels)

        # Clean and validate input
        cleaned_levels = []
        for p in price_levels:
            try:
                price = float(p[0])
                size = float(p[1])
                cleaned_levels.append([price, size])
            except (ValueError, TypeError) as e:
                print("Skipping invalid row:", p)

        if not cleaned_levels:
            raise ValueError("No valid price levels provided")

        prices = np.array([p[0] for p in cleaned_levels])
        volumes = np.array([p[1] for p in cleaned_levels])

        cumulative_volume = np.cumsum(volumes)
        fill_index = np.argmax(cumulative_volume >= quantity)
        execution_price = prices[fill_index] if fill_index < len(prices) else prices[-1]
        mid_price = (prices[0] + prices[-1]) / 2

        slippage = abs(execution_price - mid_price) / mid_price
        return round(slippage * 100, 4)  # percent

    except Exception as e:
        raise ValueError(f"Slippage estimation failed: {e}")


# --- Fee Model ---
def estimate_fee(fee_tier, quantity):
    """
    Estimate fees based on fee tier and quantity.

    Args:
        fee_tier (str): Fee tier string like 'tier_1', 'tier_2', etc.
        quantity (float): Order quantity.

    Returns:
        float: Fee amount in dollars.
    """
    fee_map = {
        'tier_1': 0.001,  # 0.1%
        'tier_2': 0.0007, # 0.07%
        'tier_3': 0.0005  # 0.05%
    }
    rate = fee_map.get(fee_tier.lower(), 0.001)
    return round(quantity * rate, 4)

# --- Market Impact (Almgren-Chriss Simplified) ---
def estimate_market_impact(volatility, quantity, liquidity=1000000):
    """
    Estimate market impact based on volatility and quantity.

    Args:
        volatility (float): Volatility of the asset.
        quantity (float): Order quantity.
        liquidity (float): Market liquidity (default 1,000,000).

    Returns:
        float: Market impact cost.
    """
    sigma = float(volatility)
    q = float(quantity)
    L = float(liquidity)

    impact = (sigma * q) / (L + 1e-8)
    return round(impact, 4)

# --- Maker/Taker Proportion Model ---
_logistic_model = LogisticRegression()

def train_maker_taker_model():
    """
    Train a simple logistic regression model to estimate maker/taker probability
    from slippage.
    """
    X = np.array([[0.01], [0.02], [0.03], [0.05], [0.08], [0.13]])  # slippage
    y = [0, 0, 0, 1, 1, 1]  # 0 = maker, 1 = taker
    _logistic_model.fit(X, y)

def predict_maker_taker(slippage):
    """
    Predict probability of taker given slippage using logistic regression.

    Args:
        slippage (float): Slippage percentage.

    Returns:
        float: Probability of taker (0 to 1).
    """
    return float(_logistic_model.predict_proba([[slippage]])[0][1])

# Call train once on module load
train_maker_taker_model()
