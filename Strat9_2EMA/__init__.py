from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Strat9_2EMA(Strategy):
	# def before(self):
	# 	self.log("------START OF CANDLE------")

	# --- HYPERPARAMETERS ---

	# def hyperparameters(self):
	# 	return [
	# 		{'name': 'donchian_period_h', 'type': int, 'min': 30, 'max': 210, 'default': 40},
	# 		{'name': 'lookback_verifying_h', 'type': int, 'min': 2, 'max': 30, 'default': 5},
	# 	]

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		self.vars["donchian_period"] = 100
		self.vars["ema_min_volatility_distance"] = 0
		self.vars["lookback_verifying"] = -30

	# --- INDICATORS ---

	@property
	def donchian(self):
		return ta.donchian(self.candles[:-1], period=self.vars["donchian_period"], sequential=True)
	@property
	def ema_1(self):
		return ta.ema(self.candles, period=100, sequential=True)
	@property
	def ema_2(self):
		return ta.ema(self.candles, period=200, sequential=True)
	@property
	def ema_3(self):
		return ta.ema(self.candles, period=300, sequential=True)
	@property
	def ema_4(self):
		return ta.ema(self.candles, period=400, sequential=True)
	@property
	def ema_5(self):
		return ta.ema(self.candles, period=500, sequential=True)
	@property
	def ema_6(self):
		return ta.ema(self.candles, period=600, sequential=True)
	@property
	def ema_7(self):
		return ta.ema(self.candles, period=700, sequential=True)

	# --- FILTERS ---

	def trend_filter(self):
		if self.ema_1[-1] > \
			self.ema_2[-1] > \
			self.ema_3[-1] > \
			self.ema_4[-1] > \
			self.ema_5[-1] > \
			self.ema_6[-1] > \
			self.ema_7[-1] or \
			self.ema_1[-1] < \
			self.ema_2[-1] < \
			self.ema_3[-1] < \
			self.ema_4[-1] < \
			self.ema_5[-1] < \
			self.ema_6[-1] < \
			self.ema_7[-1]:
			return True

	def volatility_filter(self):
		perc = abs((self.ema_1[-1] - self.ema_2[-1]) / (self.ema_2[-1] / 100))
		return perc > self.vars["ema_min_volatility_distance"]

	def filters(self):
		return [self.trend_filter, self.volatility_filter]

	# --- ORDERS ---

	def should_long(self) -> bool:
		d_lookback = self.vars["lookback_verifying"]
		if list(self.donchian.lowerband[-1:d_lookback:-1]).count(self.donchian.lowerband[-1]) == len(
				self.donchian.lowerband[-1:d_lookback:-1]) \
				and self.ema_2[-1] > self.ema_1[-1] > self.close:
			return True



	def should_short(self) -> bool:

		d_lookback = self.vars["lookback_verifying"]
		if list(self.donchian.upperband[-1:d_lookback:-1]).count(self.donchian.upperband[-1]) == len(
				self.donchian.upperband[-1:d_lookback:-1]) \
				and self.ema_2[-1] < self.ema_1[-1] < self.close:
			return True

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):
		d_lookback = self.vars["lookback_verifying"]
		entry = min(self.donchian.lowerband[-1:d_lookback:-1])

		# 	StopLoss = 2x ATR
		stop = entry - (max(self.donchian.upperband[-1:d_lookback:-1]) - min(self.donchian.lowerband[-1:d_lookback:-1]))

		# 	TakeProfit = 5x ATR
		profit_target = max(self.donchian.upperband[-1:d_lookback:-1])

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

		# 	Buy action
		self.buy = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	def go_short(self):
		d_lookback = self.vars["lookback_verifying"]
		entry = max(self.donchian.upperband[-1:d_lookback:-1])

		# 	StopLoss = 2x ATR
		stop = entry + (max(self.donchian.upperband[-1:d_lookback:-1]) - min(self.donchian.lowerband[-1:d_lookback:-1]))

		# 	TakeProfit = 5x ATR
		profit_target = min(self.donchian.lowerband[-1:d_lookback:-1])

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	# --- LOGS - --

	# def after(self):
	# 	self.log("-- PARAMETERS")
	# 	self.log("")
	#
	# 	self.log(f"UPPER-bands: LAST {self.donchian.upperband[-1]} ALL: {list(self.donchian.upperband[-1:-20:-1])}")
	# 	if list(self.donchian.upperband[-1:-20:-1]).count(self.donchian.upperband[-1]) == len(self.donchian.upperband[-1:-20:-1]):
	# 		self.log("all last values THE SAME")
	# 	else:
	# 		self.log("no same values")
	# 	self.log("")
	#
	# 	self.log(f"LOWER-bands: LAST {self.donchian.lowerband[-1]} ALL: {list(self.donchian.lowerband[-1:-20:-1])}")
	# 	if list(self.donchian.lowerband[-1:-20:-1]).count(self.donchian.lowerband[-1]) == len(self.donchian.lowerband[-1:-20:-1]):
	# 		self.log("all last values THE SAME")
	# 	else:
	# 		self.log("no same values")
	# 	self.log("")
	#
	# 	self.log("Local TREND is {}".format((lambda fast, slow:
	# 	f"BULL-ish and last UPPERdonchian is: {self.donchian.upperband[-1]}" if fast > slow
	# 	else f"BULL-ish and last LOWERdonchian is: {self.donchian.upperband[-1]}")(self.ema_1[-1], self.ema_2[-1])))
	# 	self.log("")
	#
	# 	self.log("------END OF CANDLE------")