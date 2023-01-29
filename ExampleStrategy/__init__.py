from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class ExampleStrategy(Strategy):
    def before(self):
        c_open = self.candles[:, 1]
        c_close = self.candles[:, 2]
        c_high = self.candles[:, 3]
        c_low = self.candles[:, 4]

        def percentCounter(candleIndex):
            return abs(c_open[-candleIndex] - c_close[-candleIndex]) / (
                        abs(c_high[-candleIndex] - c_low[-candleIndex]) / 100)

        total_candles = 5
        filter_percent = 70

        '''


        sumOfShadowRange = []
        candleTotalRange = abs(c_open[-total_candles] - c_close[-1])
        bodyShadowPercent = []

        for i in range(1, total_candles):
            sumOfShadowRange.append(abs(c_high[-i] - c_low[-i]))

        for i in range(1, total_candles):
            bodyShadowPercent.append((abs(c_open[-i] - c_close[-i]) / (abs(c_high[-i] - c_low[-i]) / 100)) / 100)

        bodyShadowPercentAvg = sum(bodyShadowPercent) / len(bodyShadowPercent)

        movement_index = (sum(sumOfShadowRange) / candleTotalRange) / bodyShadowPercentAvg

        if movement_index < 10:
            self.log(f"------ Index: {movement_index}")
        '''

        #
        # oneWayCandlesPercent = []
        #
        # for i in range(1, total_candles):
        #     if percentCounter(i) > filter_percent and percentCounter(i+1) > filter_percent and percentCounter(i+2) > filter_percent:
        #         if (c_close[-i] > c_open[-i] and c_close[-i-1] > c_open[-i-1] and c_close[-i-2] > c_open[-i-2]) or \
        #             (c_close[-i] < c_open[-i] and c_close[-i-1] < c_open[-i-1] and c_close[-i-2] < c_open[-i-2]):
        #             oneWayCandlesPercent.append(1)
        #
        # movement_index = sum(oneWayCandlesPercent)
        #
        # if movement_index > 0 :
        #     self.log(f"------ Index: {movement_index}")

        if percentCounter(1) > filter_percent and percentCounter(2) > filter_percent and percentCounter(
                3) > filter_percent:
            if (c_close[-1] > c_open[-1] and c_close[-2] > c_open[-2] and c_close[-3] > c_open[-3]) or \
                    (c_close[-1] < c_open[-1] and c_close[-2] < c_open[-2] and c_close[-3] < c_open[-3]):
                self.log(f"------ THREE RAILS")

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

