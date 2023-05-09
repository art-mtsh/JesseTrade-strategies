from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Strat20_PinBar_10EMA(Strategy):

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()
		self.vars["start_bal"] = 100
		# 10EMA basis
		self.vars["emabasis"] = 10
		# 10EMA delta
		self.vars["emadelta"] = 10
		# Середній ATR останніх 10 барів в %
		self.vars["atr10min"] = 0.1
		# мінімальний рендж пін-бару
		self.vars["taillong_min"] = 0.1
		# максимальний рендж пін-бару
		self.vars["taillong_max"] = 2.0
		# тіло до хвоста у %
		self.vars["br_ratio"] = 15
		# наскільки близько до краю має бути тіло
		self.vars["body_position"] = 7
		# кімната зліва
		self.vars["room"] = 1
		# risk/reward ratio
		self.vars["RR"] = 1

	# --- INDICATORS ---
	@property
	def ema1(self):
		return ta.ema(self.candles, period=self.vars["emabasis"] + self.vars["emadelta"] * 0, sequential=False)
	@property
	def ema2(self):
		return ta.ema(self.candles, period=self.vars["emabasis"] + self.vars["emadelta"] * 1, sequential=False)
	@property
	def ema3(self):
		return ta.ema(self.candles, period=self.vars["emabasis"] + self.vars["emadelta"] * 2, sequential=False)
	@property
	def ema4(self):
		return ta.ema(self.candles, period=self.vars["emabasis"] + self.vars["emadelta"] * 3, sequential=False)
	@property
	def ema5(self):
		return ta.ema(self.candles, period=self.vars["emabasis"] + self.vars["emadelta"] * 4, sequential=False)
	@property
	def ema6(self):
		return ta.ema(self.candles, period=self.vars["emabasis"] + self.vars["emadelta"] * 5, sequential=False)
	@property
	def ema7(self):
		return ta.ema(self.candles, period=self.vars["emabasis"] + self.vars["emadelta"] * 6, sequential=False)
	@property
	def ema8(self):
		return ta.ema(self.candles, period=self.vars["emabasis"] + self.vars["emadelta"] * 7, sequential=False)
	@property
	def ema9(self):
		return ta.ema(self.candles, period=self.vars["emabasis"] + self.vars["emadelta"] * 8, sequential=False)
	@property
	def ema10(self):
		return ta.ema(self.candles, period=self.vars["emabasis"] + self.vars["emadelta"] * 9, sequential=False)
	@property
	def atr10(self):
		return ta.atr(self.candles, period=10, sequential=False)

	# --- FILTERS ---

	# Фільтр 10EMA
	def ema10_filter(self):
		if self.ema1 > self.ema2 > self.ema3 > self.ema4 > self.ema5 > self.ema6 > self.ema7 > self.ema8 > self.ema9 > self.ema10 \
			or self.ema1 < self.ema2 < self.ema3 < self.ema4 < self.ema5 < self.ema6 < self.ema7 < self.ema8 < self.ema9 < self.ema10:
			return True
	# Фільтр ATR
	def atr10_filter(self):
		return (self.atr10 / (self.close / 100)) >= self.vars["atr10min"]
	# Обмеження мінімального ренджа від high До low у %
	def taillongmin_filter(self):
		return (self.high - self.low) / (self.close / 100) >= self.vars["taillong_min"]
	# Обмеження мінімального ренджа від high До low у %
	def taillongmax_filter(self):
		return (self.high - self.low) / (self.close / 100) <= self.vars["taillong_max"]
	# Наскільки хвіст має бути більшим з тіло
	def brratio_filter(self):
		return abs(self.open - self.close) / ((self.high - self.low) / 100) <= self.vars["br_ratio"]
	# Порівняння об'єму поточного бару і попереднього
	def volume_filter(self):
		candles_volume = self.candles[:, 5]
		return candles_volume[-1] >= 3 * candles_volume[-2]
	# Сума усіх фільтрів
	def filters(self):
		return [self.ema10_filter, self.atr10_filter, self.taillongmin_filter, self.taillongmax_filter, self.brratio_filter, self.volume_filter]

	# --- DECISION MAKING ---

	def should_long(self) -> bool:
		candles_low = self.candles[:, 4]
		if self.close > (self.high - (self.high - self.low) / self.vars["body_position"]) and \
			candles_low[0] <= min(candles_low[-1:-self.vars["room"]-1:-1]) and \
			self.ema1 > self.ema2:
			return True
	def should_short(self) -> bool:
		candles_high = self.candles[:, 3]
		if (self.low + (self.high - self.low) / self.vars["body_position"]) > self.close and \
			candles_high[0] >= max(candles_high[-1:-self.vars["room"]-1:-1]) and \
			self.ema1 < self.ema2:
			return True

	# --- ORDERS ---

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):

		# entry = (self.high + self.low) / 2
		entry = self.high + self.high * 0.00001
		stop = self.low - self.low * 0.00001
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

		# entry = (self.high + self.low) / 2
		entry = self.low - self.low * 0.00001
		stop = self.high + self.high * 0.00001
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

	# def after(self):
	# 	candles_volume = self.candles[:, 5]
	# 	self.log(f"EMA 1: {self.ema1}")
	# 	self.log(f"volume[-1]: {candles_volume[-1]}")
	# 	self.log(f"volume[-2]: {candles_volume[-2]}")
	# 	self.log(f"...")


