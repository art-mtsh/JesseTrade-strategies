from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

'''
Ідея стратегії:
Стратегія шуму.
Вхід по медіані Envelope
Вихід по екстремумам
'''

class Strat2_Envelope(Strategy):

	# --- HYPERPARAMETERS

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		# базова EMA1
		self.vars["ema_basis"] = 100

		# Envelopes multiplier %
		self.vars["enve_mpl"] = 2

		# Risk/reward
		self.vars["rr"] = 0.5

		# Start BALANCE
		self.vars["start_bal"] = 100

	# --- INDICATORS ---

	@property
	def ema1(self):
		return ta.ema(self.candles, self.vars["ema_basis"], sequential=False)

	# --- FILTERS ---

	# def trendEma(self):
	# 	return self.ema10 > \
	# 		   self.ema9 > \
	# 		   self.ema8 > \
	# 		   self.ema7 > \
	# 		   self.ema6 > \
	# 		   self.ema5 > \
	# 		   self.ema4 > \
	# 		   self.ema3 > \
	# 		   self.ema2 > \
	# 		   self.ema1 or \
	# 		   self.ema10 < \
	# 		   self.ema9 < \
	# 		   self.ema8 < \
	# 		   self.ema7 < \
	# 		   self.ema6 < \
	# 		   self.ema5 < \
	# 		   self.ema4 < \
	# 		   self.ema3 < \
	# 		   self.ema2 < \
	# 		   self.ema1
	#
	# def atrFilter(self):
	# 	return (self.vars["atr_mpl"] * self.atr0[-1]) / (self.close / 100) > 1
	#
	# def filters(self):
	# 	return [self.trendEma, self.atrFilter]

	# --- ORDERS ---

	def should_long(self) -> bool:
		return self.high < self. ema1

	def should_short(self) -> bool:
		return self.low > self.ema1

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):
		entry = self.ema1

		# 	StopLoss
		stop = self.ema1 - (self.close / 100) * self.vars["enve_mpl"]

		# 	TakeProfit
		profit_target = self.ema1 + (self.close / 100) * self.vars["enve_mpl"] * self.vars["rr"]

		# StopLoss percent
		slPercent = abs(stop - entry) / (self.close / 100)

		# 	Quantity
		qty = (self.vars["start_bal"] / slPercent) / self.close

		# 	Buy action
		self.buy = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	def go_short(self):
		entry = self.ema1

		# 	StopLoss
		stop = self.ema1 + (self.close / 100) * self.vars["enve_mpl"]

		# 	TakeProfit
		profit_target = self.ema1 - (self.close / 100) * self.vars["enve_mpl"] * self.vars["rr"]

		# StopLoss percent
		slPercent = abs(stop - entry) / (self.close / 100)

		# 	Quantity
		qty = (self.vars["start_bal"] / slPercent) / self.close

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target



	# def update_position(self):
	# 	c_close = self.candles[:, 2]
	#
	# 	qty = self.position.qty
	#
	# 	if self.is_long and \
	# 		(c_close[-1] - self.vars["atr_mpl"] * self.atr0[-1]) >= \
	# 		(c_close[-2] - self.vars["atr_mpl"] * self.atr0[-2]):
	# 		self.stop_loss = qty, self.close - self.vars["atr_mpl"] * self.atr0[-1]
	# 	elif self.is_short and \
	# 		(c_close[-1] + self.vars["atr_mpl"] * self.atr0[-1]) <= \
	# 		(c_close[-2] + self.vars["atr_mpl"] * self.atr0[-2]):
	# 		self.stop_loss = qty, self.close + self.vars["atr_mpl"] * self.atr0[-1]



	# def after(self):
	# 	self.log(f"Current RSI [-1] {ta.rsi(self.candles, period=14, source_type='close', sequential=False)}")
	# 	self.log(f"Current 4 * self.atr0[-1]: {4 * self.atr0[-1]}")
	#
	# 	self.log(f"--- possible ENTRY: {self.close}")
	# 	self.log(f"--- possible TOP: {self.high + 4 * self.atr0[-1]}")
	# 	self.log(f"--- possible BOTTOM: {self.low - 4 * self.atr0[-1]}")
