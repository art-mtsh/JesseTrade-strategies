from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class ExampleStrategy(Strategy):
    def before(self):
        pass

    def should_long(self) -> bool:
        return False

    def should_short(self) -> bool:
        return False

    def should_cancel_entry(self) -> bool:
        return False

    def go_long(self):
        pass

    def go_short(self):
        pass

    def after(self):
        c_open = self.candles[:, 1]
        c_close = self.candles[:, 2]
        c_high = self.candles[:, 3]
        c_low = self.candles[:, 4]

        total_candles = 11

        sumOfCandleRange = []
        sumOfShadowRange = []
        candleTotalRange = abs(c_open[-total_candles] - c_close[-1])
        bodyShadowPercent = []

        for i in range(1, total_candles):
            sumOfCandleRange.append(abs(c_open[-i] - c_close[-i]))

        for i in range(1, total_candles):
            sumOfShadowRange.append(abs(c_high[-i] - c_low[-i]))

        for i in range(1, total_candles):
            bodyShadowPercent.append((abs(c_open[-i] - c_close[-i]) / (abs(c_high[-i] - c_low[-i]) / 100)) / 100)



        bodyShadowPercentAvg = sum(bodyShadowPercent) / len(bodyShadowPercent)

        movement_index = (sum(sumOfShadowRange) / candleTotalRange) / bodyShadowPercentAvg

        # self.log(f"Sum of last bodies: {sum(sumOfCandleRange)}")
        # self.log(f"Sum of last shadows: {sum(sumOfShadowRange)}")
        # self.log(f"Sum of last range: {candleTotalRange}")
        # self.log("--- END ---")

        if movement_index < 3:
            self.log(f"------ Index: {movement_index}")

