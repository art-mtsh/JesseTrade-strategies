from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Strat10_RegAngle_2EMA_wPr(Strategy):

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
		self.vars["willr_period"] = 20  # self.hp['lingerangle_period_h']
		self.vars["ema_1_period"] = 200 # self.hp['ema_1_period_h']
		self.vars["ema_2_period"] = 300 # self.hp['ema_2_period_h']
		self.vars["lingerangle_filter"] = 0.085 # self.hp['lingerangle_filter_h']
		self.vars["willr_filter"] = 10  # self.hp['lingerangle_filter_h']
		self.vars["atr_period"] = 50

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
	@property
	def atr(self):
		return ta.atr(self.candles, period=self.vars["atr_period"], sequential=False)

	# --- FILTERS ---

	def distnces(self):
		return abs(self.close-self.ema_1[-1]) >= 2 * abs(self.ema_1[-1] - self.ema_2[-1])

	def atrrange(self):
		return abs(self.high - self.low) <= 1.5 * self.atr

	def filters(self):
		return [self.distnces, self.atrrange]

	# --- ORDERS v.1 ---

	# фільтр по двом ЕМА
	# фільтр по значенню перепроданності/перекупленності W%R
	# фільтр по зниженню/підвищенню значення W%R
	# фільтр по незначному ATR сигнального бара

	def should_long(self) -> bool:
		if self.close > self.ema_1[-1] > self.ema_2[-1] and \
			self.willr[-2] < (-100+self.vars["willr_filter"]) and \
			self.willr[-1] > self.willr[-2]:
			return True

	def should_short(self) -> bool:
		if self.close < self.ema_1[-1] < self.ema_2[-1] and \
			self.willr[-2] > (0-self.vars["willr_filter"]) and \
			self.willr[-1] < self.willr[-2]:
			return True

	# --- ORDERS v.2 ---

	# фільтр по двом ЕМА
	# фільтр по значенню перепроданності/перекупленності W%R
	# фільтр по типу сигнального бара

	# def should_long(self) -> bool:
	# 	if self.ema_2[-1] < self.ema_1[-1] < self.close and \
	# 		self.willr[-1] < (-100 + self.vars["willr_filter"]):
	# 		return True
	#
	# def should_short(self) -> bool:
	# 	if self.ema_2[-1] > self.ema_1[-1] > self.close and \
	# 		self.willr[-1] > (0 - self.vars["willr_filter"]):
	# 		return True
	#
	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):

		entry = self.high + 0.3 * self.atr

		# 	StopLoss
		stop = entry - 3 * self.atr

		# 	TakeProfit
		profit_target = entry + 1 * self.atr

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

		# 	Buy action
		self.buy = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	def go_short(self):

		entry = self.low - 0.3 * self.atr

		# 	StopLoss
		stop = entry + 3 * self.atr

		# 	TakeProfit
		profit_target = entry - 1 * self.atr

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target