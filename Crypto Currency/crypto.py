from agents import Agent, Runner, function_tool
from connection import config
import requests

@function_tool
def get_crypto_price(symbol: str) -> str:
    """
    Get live price for a given cryptocurrency symbol, e.g., BTCUSDT.
    """
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url)
    data = response.json()
    
    for item in data:
        if item['symbol'].upper() == symbol.upper():
            return f"The current price of {symbol.upper()} is {item['price']} USD."
    return f"Symbol {symbol.upper()} not found."

@function_tool
def get_coin_by_symbol(currency: str) -> str:
    """
    Get price for a specific symbol using direct query, e.g., BTCUSDT.
    """
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={currency.upper()}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Error fetching data for {currency.upper()}"
    
    data = response.json()
    return f"The current price of {currency.upper()} is {data['price']} USD."

# Create the agent
agent = Agent(
    name="crypto_agent",
    instructions="You are a helpful crypto assistant. Use the tools to fetch live crypto prices.",
    tools=[get_crypto_price, get_coin_by_symbol]
)

result = Runner.run_sync(
    agent,
    input="What is the price of BTCUSDT?",
    run_config=config
)

# Print the result
print(result.final_output)
