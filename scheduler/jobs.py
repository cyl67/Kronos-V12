import schedule
import time


def run_strategy():
    print("执行 AI策略")


schedule.every(5).minutes.do(run_strategy)

while True:
    schedule.run_pending()
    time.sleep(1)