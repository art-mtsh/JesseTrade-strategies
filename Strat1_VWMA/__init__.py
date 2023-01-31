from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class Strat1_VWMA(Strategy):

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		self.vars["fast_vwma"] = 60
		self.vars["slow_vwma"] = 180
		self.vars["RR"] = 1
		self.vars["rsi"] = 5
		self.vars["lower_rsi"] = 30
		self.vars["upper_rsi"] = 70
		self.vars["atr_multiplyer"] = 5
		self.vars["start_bal"] = 100

	# --- INDICATORS ---

	@property
	def vwma1(self):
		return ta.ema(self.candles, self.vars["fast_vwma"])

	@property
	def vwma2(self):
		return ta.ema(self.candles, self.vars["slow_vwma"])

	@property
	def rsi(self):
		return ta.rsi(self.candles, self.vars["rsi"])

	# --- FILTERS ---

	# фільтр ренджу останнього бару
	def percent(self):
		return (self.vars["atr_multiplyer"] * ta.atr(self.candles, 100)) / (self.close / 100) > 0.5

	# сума всіх фільтрів
	def filters(self):
		return [self.percent]

	# --- ORDERS ---

	def should_long(self) -> bool:
		return self.low > self.vwma1 > self.vwma2 and \
			   self.rsi < self.vars["lower_rsi"]

	def should_short(self) -> bool:
		return self.high < self.vwma1 < self.vwma2 and \
			   self.rsi > self.vars["upper_rsi"]

	def should_cancel_entry(self) -> bool:
		return False

	def go_long(self):
		entry = self.close

		# 	StopLoss
		stop = entry - self.vars["atr_multiplyer"] * ta.atr(self.candles, 100)

		# 	TakeProfit
		profit_target = entry + self.vars["RR"] * abs(entry - stop)

		# StopLoss percent
		slPercent = abs(stop - entry) / (self.close / 100)

		# 	Quantity to buy
		qty = (self.vars["start_bal"] / slPercent) / self.close

		# 	Buy action
		self.buy = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	def go_short(self):
		entry = self.close

		# 	StopLoss
		stop = entry + self.vars["atr_multiplyer"] * ta.atr(self.candles, 100)

		# 	TakeProfit
		profit_target = entry - self.vars["RR"] * abs(entry - stop)

		# StopLoss percent
		slPercent = abs(stop - entry) / (self.close / 100)

		# 	Quantity to buy
		qty = (self.vars["start_bal"] / slPercent) / self.close

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

# def update_position(self):
# 	if self.is_long and self.rsi > self.vars["upper_rsi"]:
# 		self.liquidate()
# 	elif self.is_short and self.rsi < self.vars["lower_rsi"]:
# 		self.liquidate()
