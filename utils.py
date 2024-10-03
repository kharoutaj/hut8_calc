def mining_cost(power_watts, electricity_rate_per_kwh):
    """
    Calculate mining cost on daily, monthly, and yearly basis.

    Parameters:
    - power_watts: Power consumption of the mining equipment (Watts)
    - electricity_rate_per_kwh: Cost of electricity per kWh (in dollars)

    Returns:
    - Daily mining cost
    - Monthly mining cost (30 days)
    - Yearly mining cost (365 days)
    """

    # Convert power consumption to kWh (1 watt = 1/1000 kilowatts)
    power_kwh = power_watts / 1000

    # Calculate daily power consumption
    daily_power_consumption = power_kwh * 24

    # Calculate daily mining cost
    daily_mining_cost = daily_power_consumption * electricity_rate_per_kwh

    # Calculate monthly and yearly costs (assuming 30 days in a month and 365 days in a year)
    monthly_mining_cost = daily_mining_cost * 30
    yearly_mining_cost = daily_mining_cost * 365

    return daily_mining_cost, monthly_mining_cost, yearly_mining_cost


def mining_revenue_usd(hash_rate_ths, network_difficulty, block_reward_btc, bitcoin_price_usd):
    """
    Calculate Bitcoin mining revenue in USD.

    Parameters:
    - hash_rate_ths: Hash rate of the mining equipment (TH/s)
    - network_difficulty: Current Bitcoin network difficulty
    - block_reward_btc: Current block reward (BTC)
    - bitcoin_price_usd: Current price of Bitcoin in USD

    Returns:
    - Daily revenue in USD
    - Monthly revenue in USD (30 days)
    - Yearly revenue in USD (365 days)
    """

    # Calculate daily revenue in BTC
    seconds_per_day = 86400
    expected_daily_btc = (hash_rate_ths * 1000000000000  * block_reward_btc * seconds_per_day) / (network_difficulty * 2 ** 32)

    # Convert BTC revenue to USD
    daily_revenue_usd = expected_daily_btc * bitcoin_price_usd

    # Calculate monthly and yearly revenue
    monthly_revenue_usd = daily_revenue_usd * 30
    yearly_revenue_usd = daily_revenue_usd * 365

    return daily_revenue_usd, monthly_revenue_usd, yearly_revenue_usd


def mining_revenue_in_btc(hash_rate_ths, network_difficulty, block_reward_btc):
    """
    Calculate Bitcoin mining revenue in BTC.

    Parameters:
    - hash_rate_ths: Hash rate of the mining equipment (TH/s)
    - network_difficulty: Current Bitcoin network difficulty
    - block_reward_btc: Current block reward (BTC)

    Returns:
    - Daily revenue in BTC
    - Monthly revenue in BTC (30 days)
    - Yearly revenue in BTC (365 days)
    """

    # Calculate daily revenue in BTC
    seconds_per_day = 86400
    expected_daily_btc = (hash_rate_ths * 1000000000000 * block_reward_btc * seconds_per_day) / (network_difficulty * 2 ** 32)

    # Calculate monthly and yearly revenue in BTC
    monthly_revenue_btc = expected_daily_btc * 30
    yearly_revenue_btc = expected_daily_btc * 365

    return expected_daily_btc, monthly_revenue_btc, yearly_revenue_btc

def breakeven_months(daily_profit, initial_investment):
    """
    Calculate breakeven timeline in months

    Parameters:
    - daily_profit: Daily profit in USD
    - inital_investment: Initial investment in USD

    Returns:
    - Number of months to breakeven or -1 if daily profit is negative
    """

    if daily_profit > 0:
        break_even_days = initial_investment / daily_profit
        break_even_months = break_even_days / 30  # Convert break-even time from days to months
    else:
        return -1
    return break_even_months


def cost_to_mine(hash_rate_ths, network_difficulty, power_watts, electricity_rate_per_kwh, block_reward_btc):
    """
    Calculate the cost to mine 1 Bitcoin (BTC) in USD.

    Parameters:
    - hash_rate_ths: Hash rate of the mining equipment (TH/s)
    - network_difficulty: Current Bitcoin network difficulty
    - power_watts: Power consumption of the mining equipment (Watts)
    - electricity_rate_per_kwh: Cost of electricity per kWh (in dollars)
    - block_reward_btc: Current block reward (BTC)

    Returns:
    - Cost to mine 1 BTC (USD)
    """

    # Calculate the daily BTC revenue from mining
    seconds_per_day = 86400
    expected_daily_btc = (hash_rate_ths * block_reward_btc * seconds_per_day) / (network_difficulty * 2 ** 32)

    # Calculate the time (in days) to mine 1 BTC
    days_to_mine_one_btc = 1 / expected_daily_btc

    # Calculate the total electricity cost for the period it takes to mine 1 BTC
    power_kwh = power_watts / 1000
    daily_power_consumption_kwh = power_kwh * 24
    total_power_consumption_kwh = daily_power_consumption_kwh * days_to_mine_one_btc
    cost_to_mine_one_btc = total_power_consumption_kwh * electricity_rate_per_kwh

    return cost_to_mine_one_btc
