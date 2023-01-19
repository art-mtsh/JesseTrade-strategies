from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class Strat1_VWMA(Strategy):

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		self.vars["max_vol_percent"] = 2
		self.vars["min_vol_percent"] = 1
		self.vars["rsi"] = 10
		self.vars["lower_rsi"] = 25
		self.vars["upper_rsi"] = 75
		self.vars["atr_multiplyer"] = 2

	# --- INDICATORS ---

	@property
	def vwma1(self):
		return ta.vwma(self.candles, 100, sequential=True)

	@property
	def vwma2(self):
		return ta.vwma(self.candles, 500, sequential=True)

	@property
	def rsi(self):
		return ta.rsi(self.candles, self.vars["rsi"])

	# --- FILTERS ---

	def volatility_filter(self):
		perc = abs((self.vwma1[-1] - self.vwma2[-1]) / (self.vwma1[-1] / 100))
		return self.vars["max_vol_percent"] > perc > self.vars["min_vol_percent"]

	def filters(self):
		return [self.volatility_filter]

	# --- ORDERS ---

	def should_long(self) -> bool:
		return self.vwma1[-1] > self.vwma2[-1] and self.rsi < self.vars["lower_rsi"]

	def should_short(self) -> bool:
		return self.vwma1[-1] < self.vwma2[-1] and self.rsi < self.vars["upper_rsi"]

	def should_cancel_entry(self) -> bool:
		return False

	def go_long(self):
		entry = self.price
		stop = entry - self.vars["atr_multiplyer"] * ta.atr(self.candles)
		profit_target = entry + self.vars["atr_multiplyer"] * ta.atr(self.candles)
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)
		self.buy = qty, entry
		self.stop_loss = qty, stop
		self.take_profit = qty, profit_target

	def go_short(self):
		entry = self.price
		stop = entry + self.vars["atr_multiplyer"] * ta.atr(self.candles)
		profit_target = entry - self.vars["atr_multiplyer"] * ta.atr(self.candles)
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)
		self.sell = qty, entry
		self.stop_loss = qty, stop
		self.take_profit = qty, profit_target

	def update_position(self):
		if self.is_long and self.rsi > self.vars["upper_rsi"]:
			self.liquidate()
		elif self.is_short and self.rsi < self.vars["lower_rsi"]:
			self.liquidate()