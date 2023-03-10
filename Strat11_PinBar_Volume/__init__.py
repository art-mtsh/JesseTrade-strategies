from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

'''
Стратегія на Н1, що базується на пінбарах

'''

class Strat11_PinBar_Volume(Strategy):

	# --- HYPERPARAMETERS ---

	def hyperparameters(self):
		return [
			{'name': 'taillong_min_h', 'type': int, 'min': 0, 'max': 0.02, 'default': 0.01},
			{'name': 'taillong_max_h', 'type': int, 'min': 0.02, 'max': 0.05, 'default': 0.03},
			{'name': 'tail_h', 'type': int, 'min': 2, 'max': 8, 'default': 5},
			{'name': 'body_position_h', 'type': int, 'min': 2, 'max': 6, 'default': 4},
		]

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		self.vars["tail"] = 4 # self.hp['tail_h']
		self.vars["taillong_min"] = 0.01 # self.hp['taillong_min_h']
		self.vars["taillong_max"] = 0.03 # self.hp['taillong_max_h']
		self.vars["body_position"] = 4 # self.hp['body_position_h']

	# --- INDICATORS ---

	# --- FILTERS ---

	# Наскільки хвіст має бути більшим з тіло
	def tail(self):
		return abs(self.high - self.low) > self.vars["tail"] * abs(self.open - self.close)
	# Обмеження мінімального і максимального ренджа від high До low у %
	def taillong(self):
		return self.close * self.vars["taillong_max"] >= abs(self.high - self.low) >= self.close * self.vars["taillong_min"]
	# Порівняння об'єму поточного бару і попереднього
	def volumefilter(self):
		candles_volume = self.candles[:, 5]
		return candles_volume[0] < candles_volume[-1]
	# Сума усіх фільтрів
	def filters(self):
		return [self.tail, self.taillong, self.volumefilter]

	# --- DECISION MAKING ---

	def should_long(self) -> bool:
		if self.high > self.close > (self.high - abs(self.high - self.low) / self.vars["body_position"]):
			return True

	def should_short(self) -> bool:
		if (self.low + abs(self.high - self.low) / self.vars["body_position"]) > self.close > self.low:
			return True

	# --- ORDERS ---

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):

		entry = self.high + self.high * 0.002

		# 	StopLoss
		stop = self.low - self.low * 0.002

		# 	TakeProfit 1/1
		profit_target1 = entry + abs(entry - stop)

		# 	TakeProfit final
		profit_target2 = entry + 2 * abs(entry - stop)

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

		# 	Buy action
		self.buy = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit 1/1
		self.take_profit = qty, profit_target1

		# 	TakeProfit final
		# self.take_profit = qty / 2, profit_target2

	def go_short(self):

		entry = self.low - self.low * 0.002

		# 	StopLoss
		stop = self.high + self.high * 0.002

		# 	TakeProfit 1/1
		profit_target1 = entry - abs(entry - stop)

		# 	TakeProfit
		profit_target2 = entry - 2 * abs(entry - stop)

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit 1/1
		self.take_profit = qty, profit_target1

		# 	TakeProfit final
		# self.take_profit = qty / 2, profit_target2