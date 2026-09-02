import numpy as np


def calculate_volatility(returns):
    daily_std = returns.std()
    annualized_vol = daily_std * np.sqrt(252)
    return annualized_vol


def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    annualized_return = returns.mean() * 252
    annualized_vol = calculate_volatility(returns)
    sharpe = (annualized_return - risk_free_rate) / annualized_vol
    return sharpe
