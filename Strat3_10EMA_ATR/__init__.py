from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

'''
Ідея стратегії:
Стратегія слідування за трендом.
Фільтр по 10 EMA.
Вхід = прорив екстремума попереднього ATR Band
Стоп = трейлінг по протилежному ATR Band
'''

class Strat3_10EMA_ATR(Strategy):

	# --- HYPERPARAMETERS

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		# базова EMA1						# для фільтру 10ЕМА
		self.vars["ema_basis"] = 100		# майже неважливо
		# дельта EMA						# які значення надаються!
		self.vars["ema_delta"] = 100		# бо основа фільтру - рендж ATR*MPL

		# ATR								# на кількість трейдів впливає опосередковано
		self.vars["atr_period"] = 200		# якісно краще брати число побільше, до 200

		# ATR multiplier					# чим менше значення - тим менше трейдів допускає фільтр
		self.vars["atr_mpl"] = 10			# оптимальне значення - 10

		# ATR filter						# чим нижче - тим більше допускається трейдів
		self.vars["atr_fil"] = 0.3			# але треба враховувати 0.1% сумарної комісії!

		# Start BALANCE
		self.vars["start_bal"] = 1000

		# Risk/Reward
		self.vars["RR"] = 1

		# reverse? 1=no, 2=yes
		self.vars["REVERSE"] = 1

	# --- INDICATORS ---

	@property
	def ema1(self):
		return ta.ema(self.candles, self.vars["ema_basis"], sequential=False)

	@property
	def ema2(self):
		return ta.ema(self.candles, self.vars["ema_basis"] + self.vars["ema_delta"], sequential=False)

	@property
	def ema3(self):
		return ta.ema(self.candles, self.vars["ema_basis"] + 2 * self.vars["ema_delta"], sequential=False)

	@property
	def ema4(self):
		return ta.ema(self.candles, self.vars["ema_basis"] + 3 * self.vars["ema_delta"], sequential=False)

	@property
	def ema5(self):
		return ta.ema(self.candles, self.vars["ema_basis"] + 4 * self.vars["ema_delta"], sequential=False)

	@property
	def ema6(self):
		return ta.ema(self.candles, self.vars["ema_basis"] + 5 * self.vars["ema_delta"], sequential=False)

	@property
	def ema7(self):
		return ta.ema(self.candles, self.vars["ema_basis"] + 6 * self.vars["ema_delta"], sequential=False)

	@property
	def ema8(self):
		return ta.ema(self.candles, self.vars["ema_basis"] + 7 * self.vars["ema_delta"], sequential=False)

	@property
	def ema9(self):
		return ta.ema(self.candles, self.vars["ema_basis"] + 8 * self.vars["ema_delta"], sequential=False)

	@property
	def ema10(self):
		return ta.ema(self.candles, self.vars["ema_basis"] + 9 * self.vars["ema_delta"], sequential=False)

	@property
	def atr0(self):
		return ta.atr(self.candles, self.vars["atr_period"], sequential=True)

	# --- FILTERS ---

	# фільтр тренду по 10 EMA
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
	# 	return (self.vars["atr_mpl"] * self.atr0[-1]) / (self.close / 100) > self.vars["atr_fil"]
	#
	# def filters(self):
	# 	return [self.trendEma, self.atrFilter]

	# --- ORDERS ---

	def should_long(self) -> bool:
		if self.vars["REVERSE"] == 1:
			return self.low > self.ema1 > self. ema2
		else:
			return self.high < self.ema1 < self.ema2

	def should_short(self) -> bool:
		if self.vars["REVERSE"] == 1:
			return self.high < self.ema1 < self. ema2
		else:
			return self.low > self.ema1 > self.ema2

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):
		if self.vars["REVERSE"] == 1:
			entry = self.close + self.vars["atr_mpl"] * self.atr0[-1]
			stop = self.close - self.vars["atr_mpl"] * self.atr0[-1]
			profit_target = entry + self.vars["RR"] * abs(entry - stop)
		else:
			entry = self.close - self.vars["atr_mpl"] * self.atr0[-1]
			profit_target = self.close + self.vars["atr_mpl"] * self.atr0[-1]
			stop = entry - self.vars["RR"] * abs(entry - profit_target)

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
		if self.vars["REVERSE"] == 1:
			entry = self.close - self.vars["atr_mpl"] * self.atr0[-1]
			stop = self.close + self.vars["atr_mpl"] * self.atr0[-1]
			profit_target = entry - self.vars["RR"] * abs(entry - stop)
		else:
			entry = self.close + self.vars["atr_mpl"] * self.atr0[-1]
			profit_target = self.close - self.vars["atr_mpl"] * self.atr0[-1]
			stop = entry + self.vars["RR"] * abs(entry - profit_target)

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
