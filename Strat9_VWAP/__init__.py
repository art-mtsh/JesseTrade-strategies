from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Strat9_VWAP(Strategy):
	# def before(self):
	# 	self.log("------START OF CANDLE------")

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
	def vwap(self):
		return ta.vwap(self.candles, source_type="hlc3", anchor="D", sequential=True)

	@property
	def atr(self):
		return ta.atr(self.candles, period=50, sequential=True)


	# --- FILTERS ---


	# --- ORDERS ---

	def should_long(self) -> bool:
		if self.vwap[-1] > self.close:
			return True


	def should_short(self) -> bool:
		if self.vwap[-1] < self.close:
			return True

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):

		entry = self.vwap[-1]

		# 	StopLoss = 2x ATR
		stop = entry - 2 * self.atr

		# 	TakeProfit = 2x ATR
		profit_target = entry + 2 * self.atr

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

		# 	Buy action
		self.buy = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	def go_short(self):

		entry = self.vwap[-1]

		# 	StopLoss = 2x ATR
		stop = entry + 2 * self.atr

		# 	TakeProfit = 2x ATR
		profit_target = entry - 2 * self.atr

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