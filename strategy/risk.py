def risk_filter(signal, max_position=1.0):
    """
    防止过度交易
    """
    if signal is None:
        return 0

    return max(min(signal, max_position), -max_position)