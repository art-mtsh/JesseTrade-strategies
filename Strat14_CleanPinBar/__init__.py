from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

'''
Стратегія на Н1, що базується на пінбарах,
які фільтруються по медіанному Дончіану та об'ємах

'''

class Strat14_CleanPinBar(Strategy):

	# --- HYPERPARAMETERS ---

	# def hyperparameters(self):
	# 	return [
			# {'name': 'donch_per_h', 'type': int, 'min': 7, 'max': 9, 'default': 8},
			# {'name': 'atr_per_h', 'type': int, 'min': 47, 'max': 49, 'default': 48},
			# {'name': 'tail_h', 'type': int, 'min': 5, 'max': 7, 'default': 6},
			# {'name': 'taillong_min_h', 'type': int, 'min': 0, 'max': 1, 'default': 0}
			# {'name': 'taillong_max_h', 'type': int, 'min': 4, 'max': 6, 'default': 5},
			# {'name': 'body_position_h', 'type': int, 'min': 3, 'max': 5, 'default': 4},
		# ]

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		# період Дончіана
		self.vars["donch_per"] = 8 # self.hp['donch_per_h']
		# тіло до хвоста
		self.vars["tail"] = 6 # self.hp['tail_h']
		# наскільки близько до краю має бути тіло
		self.vars["body_position"] =  4 # self.hp['body_position_h']

	# --- INDICATORS ---

	@property
	def donchianIndi(self):
		return ta.donchian(self.candles[:-1], period=self.vars["donch_per"], sequential=True)

	# --- FILTERS ---

	# Наскільки хвіст має бути більшим з тіло
	def tail(self):
		return abs(self.high - self.low) > self.vars["tail"] * abs(self.open - self.close)

	# Сума усіх фільтрів
	def filters(self):
		return [self.tail]

	# --- DECISION MAKING ---

	def should_long(self) -> bool:
		if self.high > self.close > (self.high - abs(self.high - self.low) / self.vars["body_position"]) and \
			self.low > self.donchianIndi.middleband[-1]:
			return True
	def should_short(self) -> bool:
		if (self.low + abs(self.high - self.low) / self.vars["body_position"]) > self.close > self.low and \
			self.high < self.donchianIndi.middleband[-1]:
			return True

	# --- ORDERS ---

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):

		entry = (self.high + self.low) / 2

		# 	StopLoss
		stop = self.low - self.low * 0.001

		# 	TakeProfit 1/1
		profit_target1 = entry + 2 * abs(entry - stop)

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 30, entry, stop, self.fee_rate)

		# 	Buy action
		self.buy = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit 1/1
		self.take_profit = qty, profit_target1

		# 	TakeProfit final
		# self.take_profit = qty / 2, profit_target2

	def go_short(self):

		entry = (self.high + self.low) / 2

		# 	StopLoss
		stop = self.high + self.high * 0.001

		# 	TakeProfit 1/1
		profit_target1 = entry - 2 * abs(entry - stop)

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 30, entry, stop, self.fee_rate)

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit 1/1
		self.take_profit = qty, profit_target1

		# 	TakeProfit final
		# self.take_profit = qty / 2, profit_target2

	def update_position(self):
		if self.is_long:
			self.stop_loss = self.position.qty, self.donchianIndi.lowerband[-1]
		elif self.is_short:
			self.stop_loss = self.position.qty, self.donchianIndi.upperband[-1]