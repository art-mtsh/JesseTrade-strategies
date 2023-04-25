from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Strat20_PinBar(Strategy):

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()
		self.vars["start_bal"] = 200

		# Середній ATR останніх 10 барів в %
		self.vars["atr10min"] = 0.2
		# мінімальний рендж пін-бару
		self.vars["taillong_min"] = 0.3
		# максимальний рендж пін-бару
		self.vars["taillong_max"] = 1.2
		# тіло до хвоста у %
		self.vars["br_ratio"] = 33
		# наскільки близько до краю має бути тіло
		self.vars["body_position"] = 3
		# кімната зліва
		self.vars["room"] = 48
		# risk/reward ratio
		self.vars["RR"] = 6

	# --- INDICATORS ---

	@property
	def atr10(self):
		return ta.atr(self.candles, period=10, sequential=False)

	# --- FILTERS ---

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
		return candles_volume[0] >= candles_volume[-1] - candles_volume[-1] * 0.1 and candles_volume[0] >= candles_volume[-2] - candles_volume[-2] * 0.1
	# Сума усіх фільтрів
	def filters(self):
		return [self.atr10_filter, self.taillongmin_filter, self.taillongmax_filter, self.brratio_filter, self.volume_filter]

	# --- DECISION MAKING ---

	def should_long(self) -> bool:
		candles_low = self.candles[:, 4]
		if self.high >= min(self.close, self.open) > (self.high - (self.high - self.low) / self.vars["body_position"]) and candles_low[0] <= min(candles_low[-1:-self.vars["room"]-1:-1]):
			return True
	def should_short(self) -> bool:
		candles_high = self.candles[:, 3]
		if (self.low + (self.high - self.low) / self.vars["body_position"]) > max(self.close, self.open) >= self.low and candles_high[0] >= max(candles_high[-1:-self.vars["room"]-1:-1]):
			return True

	# --- ORDERS ---

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):

		entry = (self.high + self.low) / 2
		stop = self.low - self.low * 0.001
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

		entry = (self.high + self.low) / 2
		stop = self.high + self.high * 0.001
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

	def after(self):
		self.log(f"Current ATR: {self.atr10 / (self.close / 100)}")
