from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class Strat1_VWMA(Strategy):

	# --- INDICATORS ---

	@property
	def vwma1(self):
		return ta.vwma(self.candles, 100, sequential=True)

	@property
	def vwma2(self):
		return ta.vwma(self.candles, 500, sequential=True)

	@property
	def rsi(self):
		return ta.rsi(self.candles, 10)

	# --- FILTERS ---

	def up1(self):
		perc = abs((self.vwma1[-1] - self.vwma2[-1]) / (self.vwma1[-1] / 100))
		return 2 > perc > 1

	def up2(self):
		return self.vwma1[-1] < self.vwma2[-1]

	def filters(self):
		return [self.up1, self.up2]

	# --- ORDERS ---

	def should_long(self) -> bool:
		return self.rsi < 30

	def should_short(self) -> bool:
		pass

	def should_cancel_entry(self) -> bool:
		return False

	def go_long(self):
		qty = utils.size_to_qty(self.balance * 2, self.price, fee_rate=self.fee_rate)
		self.buy = qty, self.price

	def go_short(self):
		pass

	def update_position(self):
		if self.is_long:
			if self.rsi > 70:
				self.liquidate()
