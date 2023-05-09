from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Strat21_InsideBar_10EMA(Strategy):

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()
		self.vars["start_bal"] = 20
		# 10EMA basis
		self.vars["emabasis"] = 100
		# 10EMA delta
		self.vars["emadelta"] = 100

		# Середній ATR останніх 10 барів в %
		self.vars["atr10min"] = 0.0

		# мінімальний рендж inbar
		self.vars["inbar_min"] = 0.10
		# максимальний рендж inar
		self.vars["inbar_max"] = 5.0

		# мінімальний рендж parent bar
		self.vars["parent_min"] = 0.8
		# максимальний рендж parent bar
		self.vars["parent_max"] = 5.0

		# відношення ренджу parent до inside bar
		self.vars["parent_to_ib_filter"] = 3

		# тіло до хвоста у %
		self.vars["br_ratio"] = 60

		# risk/reward ratio
		self.vars["RR"] = 1

		# volume multimlier filter
		self.vars["vol_mpl"] = 0

		# ema on/off filter
		# self.vars["ema_on"] = 1

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

	# Обмеження мінімального ренджа inside bar від high До low у %
	def inbarmin_filter(self):
		candles_open = self.candles[:, 1]
		candles_close = self.candles[:, 2]
		candles_high = self.candles[:, 3]
		candles_low = self.candles[:, 4]
		return abs(candles_open[-1] - candles_close[-1]) / (candles_close[-1] / 100) >= self.vars["inbar_min"]
	# Обмеження мінімального ренджа inside bar від high До low у %
	def inbarmax_filter(self):
		candles_open = self.candles[:, 1]
		candles_close = self.candles[:, 2]
		candles_high = self.candles[:, 3]
		candles_low = self.candles[:, 4]
		return abs(candles_open[-1] - candles_close[-1]) / (candles_close[-1] / 100) <= self.vars["inbar_max"]

	# Мін рендж parent bar
	def parent_min(self):
		candles_open = self.candles[:, 1]
		candles_close = self.candles[:, 2]
		candles_high = self.candles[:, 3]
		candles_low = self.candles[:, 4]
		return abs(candles_open[-2] - candles_close[-2]) / (candles_close[-2] / 100) >= self.vars["parent_min"]
	# Макс рендж parent bar
	def parent_max(self):
		candles_open = self.candles[:, 1]
		candles_close = self.candles[:, 2]
		candles_high = self.candles[:, 3]
		candles_low = self.candles[:, 4]
		return abs(candles_open[-2] - candles_close[-2]) / (candles_close[-2] / 100) <= self.vars["parent_max"]

	# співвідношення розміру ib до parent bar
	def parent_to_ib(self):
		candles_open = self.candles[:, 1]
		candles_close = self.candles[:, 2]
		candles_high = self.candles[:, 3]
		candles_low = self.candles[:, 4]
		return (abs(candles_open[-2] - candles_close[-2]) / (candles_close[-2] / 100)) / (abs(candles_open[-1] - candles_close[-1]) / (candles_close[-1] / 100)) >= self.vars["parent_to_ib_filter"]

	# Наскільки хвіст має бути більшим з тіло
	def min_brratio(self):
		candles_open = self.candles[:, 1]
		candles_close = self.candles[:, 2]
		candles_high = self.candles[:, 3]
		candles_low = self.candles[:, 4]
		ib = abs(candles_open[-1] - candles_close[-1]) / ((candles_high[-1] - candles_low[-1]) / 100)
		pb = abs(candles_open[-2] - candles_close[-2]) / ((candles_high[-2] - candles_low[-2]) / 100)
		return min(ib, pb) >= self.vars["br_ratio"]

	# Порівняння об'єму поточного бару і попереднього
	def volume_filter(self):
		candles_volume = self.candles[:, 5]
		return candles_volume[-1] >= self.vars["vol_mpl"] * candles_volume[-2]

	# Сума усіх фільтрів
	def filters(self):
		return [self.ema10_filter, self.atr10_filter, self.inbarmin_filter, self.inbarmax_filter, self.parent_min, self.parent_max, self.parent_to_ib, self.min_brratio, self.volume_filter]

	# --- DECISION MAKING ---

	def should_long(self) -> bool:
		candles_open = self.candles[:, 1]
		candles_close = self.candles[:, 2]
		if self.ema1 > self.ema2 and candles_open[-2] < candles_open[-1] <= candles_close[-2] and candles_open[-2] < candles_close[-1] < candles_close[-2]:
			return True

	def should_short(self) -> bool:
		candles_open = self.candles[:, 1]
		candles_close = self.candles[:, 2]
		if self.ema1 < self.ema2 and candles_open[-2] > candles_open[-1] >= candles_close[-2] and candles_open[-2] > candles_close[-1] > candles_close[-2]:
			return True

	# --- ORDERS ---

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):
		candles_open = self.candles[:, 1]
		candles_close = self.candles[:, 2]
		candles_high = self.candles[:, 3]
		candles_low = self.candles[:, 4]
		candles_volume = self.candles[:, 5]

		# entry = (self.high + self.low) / 2
		entry = candles_open[-1]
		stop = candles_close[-1]
		profit_target = entry + self.vars["RR"] * abs(entry - stop)

		# StopLoss percent
		slPercent = abs(stop - entry) / (candles_close[-1] / 100)

		# 	Quantity to buy
		qty = (self.vars["start_bal"] / slPercent) / candles_close[-1]

		# 	Buy action
		self.buy = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	def go_short(self):
		candles_open = self.candles[:, 1]
		candles_close = self.candles[:, 2]
		candles_high = self.candles[:, 3]
		candles_low = self.candles[:, 4]
		candles_volume = self.candles[:, 5]

		# entry = (self.high + self.low) / 2
		entry = candles_open[-1]
		stop = candles_close[-1]
		profit_target = entry - self.vars["RR"] * abs(entry - stop)

		# StopLoss percent
		slPercent = abs(stop - entry) / (candles_close[-1] / 100)

		# 	Quantity to buy
		qty = (self.vars["start_bal"] / slPercent) / candles_close[-1]

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	# def after(self):
	# 	candles_open = self.candles[:, 1]
	# 	candles_close = self.candles[:, 2]
	# 	candles_high = self.candles[:, 3]
	# 	candles_low = self.candles[:, 4]
	# 	candles_volume = self.candles[:, 5]
	# 	self.log(f"Inbar OHLC: {candles_open[-1]}, {candles_high[-1]}, {candles_low[-1]}, {candles_close[-1]}")
	# 	self.log(f"Parent OHLC: {candles_open[-2]}, {candles_high[-2]}, {candles_low[-2]}, {candles_close[-2]}")
	# 	self.log(f"EMA: {self.ema1}, {self.ema2}, {self.ema3}, {self.ema4}, {self.ema5}, {self.ema6}, {self.ema7}, {self.ema8}, {self.ema9}, {self.ema10}")
	# 	self.log(f"ATR10: {self.atr10}")
	# 	self.log(f"Inbar range: {abs(candles_open[-1] - candles_close[-1]) / (candles_close[-1] / 100)}")
	# 	self.log(f"Parent bar: {abs(candles_open[-2] - candles_close[-2]) / (candles_close[-2] / 100)}")
	# 	self.log(f"Parent to inbar: {(abs(candles_open[-2] - candles_close[-2]) / (candles_close[-2] / 100)) / (abs(candles_open[-1] - candles_close[-1]) / (candles_close[-1] / 100))}")
	# 	self.log(f"Inbar B/R ratio: {abs(candles_open[-1] - candles_close[-1]) / ((candles_high[-1] - candles_low[-1]) / 100)}")
	# 	self.log(f"Parent B/R ratio: {abs(candles_open[-2] - candles_close[-2]) / ((candles_high[-2] - candles_low[-2]) / 100)}")
	# 	self.log(f"Inbar volume: {candles_volume[-1]}")
	# 	self.log(f"Parent volume: {candles_volume[-2]}")
	# 	self.log(f"...")