from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Strat9_VWAP(Strategy):

	# --- HYPERPARAMETERS ---

	# def hyperparameters(self):
	# 	return [
	# 		{'name': 'donchian_period_h', 'type': int, 'min': 30, 'max': 210, 'default': 40},
	# 		{'name': 'lookback_verifying_h', 'type': int, 'min': 2, 'max': 30, 'default': 5},
	# 	]

	# --- CUSTOM VARIABLES ---
	#
	# def __init__(self):
	# 	super().__init__()
	#
	# 	self.vars["donchian_period"] = 100
	# 	self.vars["ema_min_volatility_distance"] = 0
	# 	self.vars["lookback_verifying"] = -30

	# --- INDICATORS ---

	@property
	def lingerangle(self):
		return ta.linearreg_angle(self.candles, period = 14, source_type = "close", sequential=True)
	@property
	def ema_1(self):
		return ta.ema(self.candles, period=400, sequential=True)
	@property
	def ema_2(self):
		return ta.ema(self.candles, period=600, sequential=True)


	# --- FILTERS ---


	# --- ORDERS ---

	def should_long(self) -> bool:
		if self.close > self.ema_1[-1] > self.ema_2[-1] and \
			self.lingerangle[-1] < -0.055:
			return True


	def should_short(self) -> bool:
		if self.close < self.ema_1[-1] < self.ema_2[-1] and \
			self.lingerangle[-1] > 0.055:
			return True

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):

		entry = self.close

		# 	StopLoss
		stop = self.ema_2[-1]

		# 	TakeProfit
		profit_target = entry + abs(self.close - self.ema_2[-1])

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

		# 	Buy action
		self.buy = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	def go_short(self):

		entry = self.close

		# 	StopLoss
		stop = self.ema_2[-1]

		# 	TakeProfit
		profit_target = entry - abs(self.close - self.ema_2[-1])

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target