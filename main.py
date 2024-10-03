import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from utils import mining_cost, mining_revenue_usd, mining_revenue_in_btc, breakeven_months, cost_to_mine


class CalcParams(BaseModel):
    hash_rate: float
    electricity_cost: float
    power_consumption: float
    initial_investment: float

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_btc_stats():
    """
    Use blockchain query api to gather relevant BTC stats

    Returns:
    - Mining block reward
    - Mining difficulty
    - 24 hour weighted BTC price in USD
    """
    block_reward = float(requests.get(url="https://blockchain.info/q/bcperblock").json())
    difficulty = float(requests.get(url="https://blockchain.info/q/getdifficulty").json())
    exchange_rate = float(requests.get(url="https://blockchain.info/q/24hrprice").json())
    return block_reward, difficulty, exchange_rate

@app.post("/calculate/")
def calculate_profit(params: CalcParams):
    # get BTC stats and then call util methods to run calcs
    reward, difficulty, exchange_rate = get_btc_stats()
    daily_cost, monthly_cost, yearly_cost = mining_cost(params.power_consumption, params.electricity_cost)
    daily_rev_usd, monthly_rev_usd, yearly_rev_usd = mining_revenue_usd(params.hash_rate, difficulty, reward, exchange_rate)
    daily_rev_btc, monthly_rev_btc, yearly_rev_btc = mining_revenue_in_btc(params.hash_rate, difficulty, reward)
    breakeven = breakeven_months(daily_cost, params.initial_investment)
    one_btc_cost = cost_to_mine(params.hash_rate, difficulty, params.power_consumption, params.electricity_cost, reward)

    results = {
        "dailyCost": daily_cost,
        "monthlyCost": monthly_cost,
        "yearlyCost": yearly_cost,
        "dailyRevenueUSD": daily_rev_usd,
        "monthlyRevenueUSD": monthly_rev_usd,
        "yearlyRevenueUSD": yearly_rev_usd,
        "dailyRevenueBTC": daily_rev_btc,
        "monthlyRevenueBTC": monthly_rev_btc,
        "yearlyRevenueBTC": yearly_rev_btc,
        "dailyProfitUSD": daily_rev_usd - daily_cost,
        "monthlyProfitUSD": monthly_rev_usd - monthly_cost,
        "yearlyProfitUSD": yearly_rev_usd - yearly_cost,
        "breakevenTimeline": breakeven,
        "costToMine": one_btc_cost
    }

    return JSONResponse(status_code=200, content=results)
