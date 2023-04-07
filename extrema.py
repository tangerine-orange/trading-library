def find_local_extrema(data, start_index, sma_close, window_size=5, sensitivity=0.03):
    if sma_close[start_index] is None:
        return []

    extrema_points = []
    for i, candle in enumerate(data):
        current_close = float(candle["close"])

        if current_close >= sma_close[start_index + i] * (1 + sensitivity):
            extrema_points.append({"type": "local_maximum", "value": current_close, "index": start_index + i})

        if current_close <= sma_close[start_index + i] * (1 - sensitivity):
            extrema_points.append({"type": "local_minimum", "value": current_close, "index": start_index + i})

    return extrema_points
