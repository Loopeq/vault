def strategy(data):
    # this is new
    signals = []
    but_threshold = 30
    sell_threshold = 70
    for index, rsi_metric in enumerate(data):
        if rsi_metric < but_threshold:
            signals.append({"index": index, "signal": "buy"})
        elif rsi_metric > sell_threshold:
            signals.append({"index": index, "signal": "sell"})
    return signals
