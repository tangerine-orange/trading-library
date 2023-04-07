import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from dotenv import load_dotenv
from bybit_api import fetch_price_data
from moving_average import simple_moving_average
from extrema import find_local_extrema

def plot_price_data(price_data, sma_window_size, interval):
    timestamps = [datetime.datetime.fromtimestamp(item["open_time"]) for item in price_data]
    close_prices = [float(item["close"]) for item in price_data]

    sma_close = [simple_moving_average(close_prices[:i+1], sma_window_size) for i in range(len(close_prices))]

    plt.figure(figsize=(15, 7))
    plt.plot(timestamps, close_prices, label='Price')
    plt.plot(timestamps, sma_close, label=f'{sma_window_size}-period SMA', linestyle='--', color='orange')

    all_extrema_points = [find_local_extrema(price_data[i:i+5], i, sma_close) for i in range(len(price_data)-4)]
    extrema_points = [point for sublist in all_extrema_points for point in sublist]

    maxima_timestamps = [timestamps[point['index']] for point in extrema_points if point['type'] == 'local_maximum']
    maxima_prices = [point['value'] for point in extrema_points if point['type'] == 'local_maximum']

    minima_timestamps = [timestamps[point['index']] for point in extrema_points if point['type'] == 'local_minimum']
    minima_prices = [point['value'] for point in extrema_points if point['type'] == 'local_minimum']

    plt.scatter(maxima_timestamps, maxima_prices, color='red', s=100, edgecolors='k', zorder=3)
    plt.scatter(minima_timestamps, minima_prices, color='green', s=100, edgecolors='k', zorder=3)

    interval_minutes = int(interval)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=interval_minutes))
    plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(interval=interval_minutes))
    plt.xlabel("Date and Time")
    plt.ylabel("Price")
    plt.title("Price History")
    plt.grid()
    plt.show()

def main():
    symbol = "BTCUSD"
    intervalNum = 1 * 60 * 4
    interval = str(intervalNum)
    start_time = int((datetime.datetime.now() - datetime.timedelta(days=30)).timestamp())
    sma_window_size = 5

    price_data = fetch_price_data(symbol, interval, start_time)
    plot_price_data(price_data, sma_window_size, interval)

if __name__ == "__main__":
    main()
