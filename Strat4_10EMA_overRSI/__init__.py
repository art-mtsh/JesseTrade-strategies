from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

'''
Ідея стратегії в реакції на 10 ЕМА
Покупка/продажа на 1ЕМА,
Стоп на 10ЕМА
Профіт на 1 RR

'''


class Strat4_10EMA_overRSI(Strategy):

	# --- HYPERPARAMETERS

	# def hyperparameters(self):
	# return [
	# {'name': 'ema1_opt', 'type': int, 'min': 100, 'max': 310, 'default': 300},
	# {'name': 'ema2_opt', 'type': int, 'min': 400, 'max': 610, 'default': 600}
	# {'name': 'rsi_opt', 'type': int, 'min': 8, 'max': 25, 'default': 10},
	# {'name': 'rsi_upper', 'type': int, 'min': 60, 'max': 90, 'default': 75},
	# {'name': 'rsi_lower', 'type': int, 'min': 10, 'max': 40, 'default': 25}
	# ]

	# --- CUSTOM VARIABLES ---

	'''
	Непоганий сет

		def __init__(self):
		super().__init__()

		# базова EMA1
		self.vars["ema_basis"] = 30
		# дельта EMA
		self.vars["ema_delta"] = 30
		# період RSI
		self.vars["rsi_period"] = 30
		# RSI min
		self.vars["rsi_min"] = 45
		# RSI max
		self.vars["rsi_max"] = 55
		# Risk/Reward
		self.vars["RR"] = 2

	'''

	def __init__(self):
		super().__init__()

		# базова EMA1
		self.vars["ema_basis"] = 50
		# дельта EMA
		self.vars["ema_delta"] = 10
		# період RSI
		self.vars["rsi_period"] = 10
		# RSI min
		self.vars["rsi_min"] = 30
		# RSI max
		self.vars["rsi_max"] = 70
		# Risk/Reward
		self.vars["RR"] = 3
		# Candles range quantity
		self.vars["c_quant"] = 8
		# Last X candles min atr range open/close
		self.vars["c_min_range"] = 0
		# Last X candles max atr range open/close
		self.vars["c_max_range"] = 1
		# Body/Range ratio %
		self.vars["BR"] = 70

		# Start BALANCE
		self.vars["start_bal"] = 5000

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
	def rsi0(self):
		return ta.rsi(self.candles, self.vars["rsi_period"], sequential=True)

	@property
	def atr0(self):
		return ta.atr(self.candles, 100, sequential=True)

	# --- FILTERS ---

	# фільтр тренду по 10 EMA
	def trendEma(self):
		return self.ema10 > \
			   self.ema9 > \
			   self.ema8 > \
			   self.ema7 > \
			   self.ema6 > \
			   self.ema5 > \
			   self.ema4 > \
			   self.ema3 > \
			   self.ema2 > \
			   self.ema1 or \
			   self.ema10 < \
			   self.ema9 < \
			   self.ema8 < \
			   self.ema7 < \
			   self.ema6 < \
			   self.ema5 < \
			   self.ema4 < \
			   self.ema3 < \
			   self.ema2 < \
			   self.ema1
	# фільтр ренджу бару по ATR
	def atrRangeCand(self):
		c_open = self.candles[:, 1]
		c_close = self.candles[:, 2]
		c_high = self.candles[:, 3]
		c_low = self.candles[:, 4]

		for i in range(0, self.vars["c_quant"]):
			if not (self.vars["c_min_range"] * self.atr0[-1] < abs(c_high[-i] - c_low[-i]) / (c_close[-i] / 100)) and \
				not (abs(c_high[-i] - c_low[-i]) / (c_close[-i] / 100) < self.vars["c_max_range"] * self.atr0[-1]):
				return False
		return True
	# фільтр співвідношення кожного тіла до ренджа
	def bodRangRatio(self):
		c_open = self.candles[:, 1]
		c_close = self.candles[:, 2]
		c_high = self.candles[:, 3]
		c_low = self.candles[:, 4]

		for i in range(0, self.vars["c_quant"]):
			if abs(c_open[-i] - c_close[-i]) / (abs(c_high[-i] - c_low[-i]) / 100) < self.vars["BR"]:
				return False
		return True
	# фільтр співвідношення середнього тіла до ренджа
	def avgBodRangRatio(self):
		c_open = self.candles[:, 1]
		c_close = self.candles[:, 2]
		c_high = self.candles[:, 3]
		c_low = self.candles[:, 4]

		percs = []

		for i in range(0, self.vars["c_quant"]):
			percs.append(abs(c_open[-i] - c_close[-i]) / (abs(c_high[-i] - c_low[-i]) / 100))

		if sum(percs) / len(percs) < self.vars["BR"]:
			return False
		return True
	# сума всіх фільтрів
	def filters(self):
		return [self.trendEma]

	# --- ORDERS ---

	def should_long(self) -> bool:
		if self.vars["REVERSE"] == 1:
			return self.ema1 < self. ema2 and abs(self.ema1 - self.ema10) > self.close * 0.01
		else:
			return self.ema1 > self.ema2 and abs(self.ema1 - self.ema10) > self.close * 0.01

	def should_short(self) -> bool:
		if self.vars["REVERSE"] == 1:
			return self.ema1 > self. ema2 and abs(self.ema1 - self.ema10) > self.close * 0.01
		else:
			return self.ema1 < self.ema2 and abs(self.ema1 - self.ema10) > self.close * 0.01

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):
		if self.vars["REVERSE"] == 1:
			entry = self.ema1
			stop = entry - abs(self.ema1 - self.ema10)
			profit_target = self.ema10
		else:
			entry = self.ema1
			stop = self.ema10
			profit_target = entry + abs(self.ema1 - self.ema10)

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
			entry = self.ema1
			stop = entry + abs(self.ema1 - self.ema10)
			profit_target = self.ema10
		else:
			entry = self.ema1
			stop = self.ema10
			profit_target = entry - abs(self.ema1 - self.ema10)

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

	# def after(self):
	# 	self.log(f"Current RSI [-1] {ta.rsi(self.candles, period=14, source_type='close', sequential=False)}")
	# 	self.log(f"Current 4 * self.atr0[-1]: {4 * self.atr0[-1]}")
	#
	# 	self.log(f"--- possible ENTRY: {self.close}")
	# 	self.log(f"--- possible TOP: {self.high + 4 * self.atr0[-1]}")
	# 	self.log(f"--- possible BOTTOM: {self.low - 4 * self.atr0[-1]}")
