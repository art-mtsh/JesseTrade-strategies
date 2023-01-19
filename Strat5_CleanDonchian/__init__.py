from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Strat5_CleanDonchian(Strategy):

	# --- HYPERPARAMETERS

	# --- INDICATORS ---

	@property
	def donchian(self):
		# Previous Donchian Channels with default parameters
		return ta.donchian(self.candles[:-1], period=100, sequential=True)

	# --- FILTERS ---

	# --- ORDERS ---


	def should_long(self) -> bool:
		return list(self.donchian.upperband[-1:-30:-1]).count(self.donchian.upperband[-1]) == len(self.donchian.upperband[-1:-30:-1])

	def should_short(self) -> bool:
		pass

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):
		entry = self.donchian.upperband[-1]

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

	def after(self):
		self.log(f"Donchian UPPER is {self.donchian.upperband[-1]}")