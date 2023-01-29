from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class Strat16_ThreeRailsREVERSE(Strategy):

	# --- HYPERPARAMETERS

	# def hyperparameters(self):
	# return [
	# {'name': 'ema1_opt', 'type': int, 'min': 100, 'max': 310, 'default': 300},
	# {'name': 'ema2_opt', 'type': int, 'min': 400, 'max': 610, 'default': 600}
	# {'name': 'rsi_opt', 'type': int, 'min': 8, 'max': 25, 'default': 10},
	# {'name': 'rsi_upper', 'type': int, 'min': 60, 'max': 90, 'default': 75},
	# {'name': 'rsi_lower', 'type': int, 'min': 10, 'max': 40, 'default': 25}
	# ]
	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		# body/shadow ratio
		self.vars["bsRatio"] = 70

		# Risk/Reward
		self.vars["RR"] = 1

	# --- INDICATORS ---

	# --- FILTERS ---

	# фільтр threeRails
	def threeRails(self):
		c_open = self.candles[:, 1]
		c_close = self.candles[:, 2]
		c_high = self.candles[:, 3]
		c_low = self.candles[:, 4]

		def percentCounter(candleIndex):
			return abs(c_open[-candleIndex] - c_close[-candleIndex]) / (
					abs(c_high[-candleIndex] - c_low[-candleIndex]) / 100)

		if percentCounter(1) > self.vars["bsRatio"] and percentCounter(2) > self.vars["bsRatio"] and percentCounter(3) > self.vars["bsRatio"]:
			if (c_close[-1] > c_open[-1] and c_close[-2] > c_open[-2] and c_close[-3] > c_open[-3]) or \
					(c_close[-1] < c_open[-1] and c_close[-2] < c_open[-2] and c_close[-3] < c_open[-3]):
				return True
	# фільтр ренджу останнього бару
	def percent(self):
		return abs(self.high - self.low) / (self.close / 100) >= 1
	# сума всіх фільтрів
	def filters(self):
		return [self.threeRails, self.percent]

	# --- DECISION MAKERS ---

	def should_long(self) -> bool:
		return self.close < self.open #and ta.ema(self.candles, 30) > ta.ema(self.candles, 100)

	def should_short(self) -> bool:
		return self.close > self.open #and ta.ema(self.candles, 30) < ta.ema(self.candles, 100)

	def should_cancel_entry(self) -> bool:
		return True

	# --- ORDERS ---

	def go_long(self):
		entry = self.low - self.low * 0.001

		# 	TakeProfit
		profit_target = abs(self.high + self.low) / 2

		# 	StopLoss
		stop = entry - self.vars["RR"] * abs(entry - profit_target)

		# StopLoss percent
		slPercent = abs(stop - entry) / (self.close / 100)

		# 	Quantity to buy
		qty = (1000 / slPercent) / self.close

		# 	Buy action
		self.buy = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	def go_short(self):
		entry = self.high + self.high * 0.001

		# 	TakeProfit
		profit_target = abs(self.high + self.low) / 2

		# 	StopLoss
		stop = entry + self.vars["RR"] * abs(entry - profit_target)

		# StopLoss percent
		slPercent = abs(stop - entry) / (self.close / 100)

		# 	Quantity to sell
		qty = (1000 / slPercent) / self.close

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	# def after(self):

