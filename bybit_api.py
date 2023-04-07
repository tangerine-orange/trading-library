import bybit
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("READ1_KEY")
api_secret = os.getenv("READ1_SECRET")

# Initialize ByBit client
client = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)

def fetch_price_data(symbol, interval, start_time, limit=200):
    kline_get_kwargs = {
        'symbol': symbol,
        'interval': interval,
        'from': start_time,
        'limit': limit,
    }
    response = client.Kline.Kline_get(**kline_get_kwargs).result()
    return response[0]["result"]