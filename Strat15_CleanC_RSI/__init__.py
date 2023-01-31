from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class Strat15_CleanC_RSI(Strategy):

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

		# період RSI
		self.vars["rsi_period"] = 10
		# RSI min
		self.vars["rsi_min"] = 35
		# RSI max
		self.vars["rsi_max"] = 65

		# CleanChart candles quantity
		self.vars["cc_quantity"] = 11
		# CleanChart filter
		self.vars["cc_filter"] = 2.5

		# Start balance
		self.vars["start_bal"] = 100
		# Risk/Reward
		self.vars["RR"] = 1
		# ATR Multiplyer for StopLoss
		self.vars["atr_multiplyer"] = 2

	# --- INDICATORS ---

	@property
	def rsi0(self):
		return ta.rsi(self.candles, self.vars["rsi_period"], sequential=True)

	@property
	def atr0(self):
		return ta.atr(self.candles, 100)

	# --- FILTERS ---

	# фільтр шуму
	def cleanChart(self):
		c_open = self.candles[:, 1]
		c_close = self.candles[:, 2]
		c_high = self.candles[:, 3]
		c_low = self.candles[:, 4]

		sumOfShadowRange = []
		candleTotalRange = abs(c_open[-self.vars["cc_quantity"]] - c_close[-1])
		bodyShadowPercent = []

		for i in range(1, self.vars["cc_quantity"]):
			sumOfShadowRange.append(abs(c_high[-i] - c_low[-i]))

		for i in range(1, self.vars["cc_quantity"]):
			bodyShadowPercent.append((abs(c_open[-i] - c_close[-i]) / (abs(c_high[-i] - c_low[-i]) / 100)) / 100)

		bodyShadowPercentAvg = sum(bodyShadowPercent) / len(bodyShadowPercent)

		movement_index = (sum(sumOfShadowRange) / candleTotalRange) / bodyShadowPercentAvg

		return movement_index <= self.vars["cc_filter"]
	# фільтр чистоти останніх двох барів до 70%
	def bodyShadow70(self):
		c_open = self.candles[:, 1]
		c_close = self.candles[:, 2]
		c_high = self.candles[:, 3]
		c_low = self.candles[:, 4]
		current_body_range_perc = (abs(c_open[-1] - c_close[-1]) / (abs(c_high[-1] - c_low[-1]) / 100))
		prev_body_range_perc = (abs(c_open[-2] - c_close[-2]) / (abs(c_high[-2] - c_low[-2]) / 100))

		return current_body_range_perc > 70 and prev_body_range_perc > 70
	# фільтр ренджу останнього бару до 3 ATR
	def midRange(self):
		return ((self.high + self.vars["atr_multiplyer"] * self.atr0) - (self.low - self.low * 0.001)) / (self.close / 100) > 0.5
	# сума всіх фільтрів
	def filters(self):
		return [self.cleanChart, self.midRange, self.bodyShadow70]

	# --- DECISION MAKERS ---

	def should_long(self) -> bool:
		return self.rsi0[-1] < self.vars["rsi_min"]

	def should_short(self) -> bool:
		return self.rsi0[-1] > self.vars["rsi_max"]

	def should_cancel_entry(self) -> bool:
		return True

	# --- ORDERS ---

	def go_long(self):
		entry = self.high + self.high * 0.001

		# 	StopLoss
		stop = self.low - self.vars["atr_multiplyer"] * self.atr0

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
		entry = self.low - self.low * 0.001

		# 	StopLoss
		stop = self.high + self.vars["atr_multiplyer"] * self.atr0

		# 	TakeProfit
		profit_target = entry - self.vars["RR"] * abs(stop - entry)

		# StopLoss percent
		slPercent = abs(stop - entry) / (self.close / 100)

		# 	Quantity to sell, using 3% risk of total account balance
		qty = (self.vars["start_bal"] / slPercent) / self.close

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	# def after(self):
	# 	c_open = self.candles[:, 1]
	# 	c_close = self.candles[:, 2]
	# 	c_high = self.candles[:, 3]
	# 	c_low = self.candles[:, 4]
	#
	# 	if self.cleanChart():
	# 		self.log(f"Close is: {self.close}")
	# 		self.log(f"Clean chart is: {self.cleanChart()}")
	# 		self.log(f"Two last body/shadow >70: {self.bodyShadow70()}")
	# 		self.log(f"Current range: {abs(self.high - self.low)}")
	# 		self.log(f"Current 3 x ATR: {3 * self.atr0[-1]}")
	# 		self.log(f"Current range is less than 3xATR: {self.midRange()}")
	# 		self.log(f"Current RSI: {self.rsi0[-1]}")
	# 		self.log("--- END OF SESSION ---")

