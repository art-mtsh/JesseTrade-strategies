from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

'''
Стратегія на Н1, що базується на BBH,
які фільтруються по медіанному Дончіану та об'ємах

'''

class Strat14_BBH(Strategy):

	# --- HYPERPARAMETERS ---

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		# період Дончіана
		self.vars["donch_per"] = 8  # self.hp['tail_h']
	# 	# тіло до хвоста
	# 	self.vars["tail"] = 6 # self.hp['tail_h']
	# 	# мінімальний рендж
	# 	self.vars["taillong_min"] = 0.01 # self.hp['taillong_min_h']
	# 	# максимальний рендж
	# 	self.vars["taillong_max"] = 1 # self.hp['taillong_max_h']
	# 	# наскільки близько до краю має бути тіло
	# 	self.vars["body_position"] = 4 # self.hp['body_position_h']

	# --- INDICATORS ---

	@property
	def donchianIndi(self):
		return ta.donchian(self.candles[:-1], period=self.vars["donch_per"], sequential=True)

	# --- FILTERS ---


	# # Наскільки хвіст має бути більшим з тіло
	# def tail(self):
	# 	return abs(self.high - self.low) > self.vars["tail"] * abs(self.open - self.close)
	# # Обмеження мінімального і максимального ренджа від high До low у %
	# def taillong(self):
	# 	return self.close * self.vars["taillong_max"] >= abs(self.high - self.low) >= self.close * self.vars["taillong_min"]
	# # Порівняння об'єму поточного бару і попереднього
	# def volumefilter(self):
	# 	candles_volume = self.candles[:, 5]
	# 	return candles_volume[0] > candles_volume[-1] and candles_volume[0] > candles_volume[-2]

	def bodyL(self):
		return (abs(self.open - self.close) / (abs(self.high - self.low) / 100)) > 90

	def volumefilter(self):
		candles_volume = self.candles[:, 5]
		return candles_volume[0] > candles_volume[-1] and candles_volume[0] > candles_volume[-2]

	# Сума усіх фільтрів
	def filters(self):
		return [self.bodyL, self.volumefilter]

	# --- DECISION MAKING ---

	def should_long(self) -> bool:
		if self.close > self.open:
			return True
	def should_short(self) -> bool:
		if self.close < self.open:
			return True

	# --- ORDERS ---

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):

		entry = self.high + self.high * 0.001

		# 	StopLoss
		stop = (self.high + self.low) / 2

		# 	TakeProfit 1/1
		profit_target1 = entry + abs(entry - stop)

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

		entry = self.low - self.low * 0.001

		# 	StopLoss
		stop = (self.high + self.low) / 2

		# 	TakeProfit 1/1
		profit_target1 = entry - abs(entry - stop)

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

	# def update_position(self):
	# 	if self.is_long:
	# 		self.stop_loss = self.position.qty, self.donchianIndi.lowerband[-1]
	# 	elif self.is_short:
	# 		self.stop_loss = self.position.qty, self.donchianIndi.upperband[-1]