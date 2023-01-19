from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils


class Strat2_EMACrossover_GIT(Strategy):
	@property
	def slow_sma(self):
		return ta.sma(self.candles, 200)

	@property
	def fast_sma(self):
		return ta.sma(self.candles, 50)

	def should_long(self) -> bool:
		# Golden Cross (reference: https://www.investopedia.com/terms/g/goldencross.asp)
		# Fast SMA above Slow SMA
		return self.fast_sma > self.slow_sma

	def should_short(self) -> bool:
		# Death Cross (reference: https://www.investopedia.com/terms/d/deathcross.asp)
		# Fast SMA below Slow SMA
		return self.fast_sma < self.slow_sma

	def should_cancel_entry(self) -> bool:
		return False

	def go_long(self):
		# Open long position and use entire balance to buy
		qty = utils.size_to_qty(self.balance, self.price, fee_rate=self.fee_rate)

		self.buy = qty, self.price

	def go_short(self):
		# Open short position and use entire balance to sell
		qty = utils.size_to_qty(self.balance, self.price, fee_rate=self.fee_rate)

		self.sell = qty, self.price

	def update_position(self):
		# If there exist long position, but the signal shows Death Cross, then close the position, and vice versa.
		if self.is_long and self.fast_sma < self.slow_sma:
			self.liquidate()

		if self.is_short and self.fast_sma > self.slow_sma:
			self.liquidate()
