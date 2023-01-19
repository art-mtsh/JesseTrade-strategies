from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Strat6_Clean10EMA(Strategy):

	# --- HYPERPARAMETERS

	# --- INDICATORS ---

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

	# --- ORDERS ---


	def should_long(self) -> bool:
		return utils.crossed(self.ema_1, self.ema_2[-1], direction="above") and self.ema_3[-1] > self.ema_4[-1] > self.ema_5[-1] > self.ema_6[-1] > self.ema_7[-1]

	def should_short(self) -> bool:
		pass

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):
		entry = self.close

	# 	StopLoss = 2x ATR
		stop = entry - 4 * ta.atr(self.candles)

	# 	TakeProfit = 5x ATR
		profit_target = entry + 4 * ta.atr(self.candles)

	# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

	# 	Buy action
		self.buy = qty, entry

	# 	StopLoss setting
		self.stop_loss = qty, stop

	# 	TakeProfit setting
		self.take_profit = qty, profit_target


	def go_short(self):
		pass
		# entry = self.donchian.lowerband[-1]
		#
		# # 	StopLoss = 2x ATR
		# stop = entry + 4 * ta.atr(self.candles)
		#
		# # 	TakeProfit = 5x ATR
		# profit_target = entry - 8 * ta.atr(self.candles)
		#
		# # 	Quantity to buy, using 3% risk of total account balance
		# qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)
		#
		# # 	Buy action
		# self.sell = qty, entry
		#
		# # 	StopLoss setting
		# self.stop_loss = qty, stop
		#
		# # 	TakeProfit setting
		# self.take_profit = qty, profit_target

	# def on_close_position(self, order):
	# 	if order.is_take_profit:
	# 		self.broker.cancel_all_orders()
	# 	elif order.is_stop_loss:
	# 		self.broker.cancel_all_orders()

	# def after(self):
	# 	self.log(f"Donchian UPPER is {self.donchian.upperband[-1]}")