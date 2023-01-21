from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Strat10_LinRegAngle_2EMA(Strategy):

	# --- HYPERPARAMETERS ---

	# def hyperparameters(self):
	# 	return [
	# 		# {'name': 'lingerangle_period_h', 'type': int, 'min': 10, 'max': 20, 'default': 14},
	# 		# {'name': 'ema_1_period_h', 'type': int, 'min': 200, 'max': 500, 'default': 400},
	# 		# {'name': 'ema_2_period_h', 'type': int, 'min': 500, 'max': 700, 'default': 600},
	# 		# {'name': 'lingerangle_filter_h', 'type': int, 'min': 0.05, 'max': 0.07, 'default': 0.055},
	# 	]

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		self.vars["lingerangle_period"] = 15 # self.hp['lingerangle_period_h']
		self.vars["willr_period"] = 100  # self.hp['lingerangle_period_h']
		self.vars["ema_1_period"] = 400 # self.hp['ema_1_period_h']
		self.vars["ema_2_period"] = 700 # self.hp['ema_2_period_h']
		self.vars["lingerangle_filter"] = 0.085 # self.hp['lingerangle_filter_h']
		self.vars["willr_filter"] = 3  # self.hp['lingerangle_filter_h']

	# --- INDICATORS ---

	@property
	def lingerangle(self):
		return ta.linearreg_angle(self.candles, period = self.vars["lingerangle_period"], source_type = "close", sequential=True)

	@property
	def willr(self):
		return ta.willr(self.candles, period = self.vars["willr_period"], sequential=True)

	@property
	def ema_1(self):
		return ta.ema(self.candles, period=self.vars["ema_1_period"], sequential=True)
	@property
	def ema_2(self):
		return ta.ema(self.candles, period=self.vars["ema_2_period"], sequential=True)


	# --- FILTERS ---

	def distnces(self):
		return abs(self.close-self.ema_1[-1]) >= 0.5 * abs(self.ema_1[-1] - self.ema_2[-1])

	def filters(self):
		return [self.distnces]

	# --- ORDERS ---

	def should_long(self) -> bool:
		if self.close > self.ema_1[-1] > self.ema_2[-1] and	self.willr[-1] < (-100+self.vars["willr_filter"]):
			return True


	def should_short(self) -> bool:
		if self.close < self.ema_1[-1] < self.ema_2[-1] and	self.willr[-1] > (0-self.vars["willr_filter"]):
			return True

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):

		entry = self.close

		# 	StopLoss
		stop = self.ema_1[-1]

		# 	TakeProfit
		profit_target = entry + 1.5 * abs(self.close - self.ema_1[-1])

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
		stop = self.ema_1[-1]

		# 	TakeProfit
		profit_target = entry - 1.5 * abs(self.close - self.ema_1[-1])

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	# def after(self):
	# 	self.log(f"Linreganle: {self.lingerangle[-1]}")
	# 	self.log(f"Ema 400: {self.ema_1[-1]}")
	# 	self.log(f"Ema 600: {self.ema_2[-1]}")