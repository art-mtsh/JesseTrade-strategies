from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class ExampleStrategy(Strategy):
    def before(self):
        self.log(f"Linear regression: {ta.linearreg(self.candles, period=14, source_type='close', sequential=False)}")
        self.log(f"Linear regression angle: {ta.linearreg_angle(self.candles, period=14, source_type='close', sequential=False)}")
        self.log(f"Linear regression intercept: {ta.linearreg_intercept(self.candles, period=14, source_type='close', sequential=False)}")
        self.log(f"Linear regression slope: {ta.linearreg_slope(self.candles, period=14, source_type='close', sequential=False)}")
        self.log("")

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
