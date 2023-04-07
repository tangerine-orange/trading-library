def simple_moving_average(data, window_size):
    if len(data) < window_size:
        return None

    return sum([float(value) for value in data[-window_size:]]) / window_size