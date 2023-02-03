from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

'''
Ідея стратегії в реакції на 10 ЕМА
Покупка/продажа на 1ЕМА,
Стоп на 10ЕМА
Профіт на 1 RR

'''


class Strat4_10EMA_overRSI_or_Williams_END(Strategy):

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
		self.vars["ema_basis"] = 100
		# дельта EMA
		self.vars["ema_delta"] = 10

		# період RSI
		self.vars["rsi_period"] = 10
		# RSI min
		self.vars["rsi_min"] = 30
		# RSI max
		self.vars["rsi_max"] = 70

		# Williams % range period
		self.vars["w%r"] = 5
		# Williams MAX
		self.vars["w%r_max"] = -1
		# Williams MIN
		self.vars["w%r_min"] = -99

		# Candles range quantity
		self.vars["c_quant"] = 4
		# Last X candles min atr range open/close
		self.vars["c_min_range"] = 0.5
		# Last X candles max atr range open/close
		self.vars["c_max_range"] = 3
		# Body/Range ratio %
		self.vars["BR"] = 50

		# Start BALANCE
		self.vars["start_bal"] = 100
		# Risk/Reward
		self.vars["RR"] = 0.5
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

	@property
	def wPr(self):
		return ta.willr(self.candles, self.vars["w%r"], sequential=True)

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
		return [self.trendEma, self.atrRangeCand, self.avgBodRangRatio]

	# --- ORDERS ---

	def should_long(self) -> bool:
		c_open = self.candles[:, 1]
		c_close = self.candles[:, 2]
		if self.vars["REVERSE"] == 1:
			return self.wPr[-1] < self.vars["w%r_min"] and \
				    c_close[-1] < c_close[-2] < c_close[-3] < c_close[-4] and \
					self.low > self.ema1 > self.ema2
		else:
			return self.wPr[-1] < self.vars["w%r_min"] and \
				    c_close[-1] < c_close[-2] < c_close[-3] < c_close[-4] and \
					self.low > self.ema1 > self.ema2


	def should_short(self) -> bool:
		c_open = self.candles[:, 1]
		c_close = self.candles[:, 2]
		if self.vars["REVERSE"] == 1:
			return self.wPr[-1] > self.vars["w%r_max"] and \
				   c_close[-1] > c_close[-2] > c_close[-3] > c_close[-4] and \
				   self.high < self.ema1 < self.ema2
		else:
			return self.wPr[-1] > self.vars["w%r_max"] and \
				   c_close[-1] > c_close[-2] > c_close[-3] > c_close[-4] and \
				   self.high < self.ema1 < self.ema2

	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):
		if self.vars["REVERSE"] == 1:
			entry = self.high + self.high * 0.0001
			stop = self.low - 0.5 * self.atr0[-1]
			profit_target = entry + abs(entry - stop) * self.vars["RR"]
		else:
			entry = self.low - self.low * 0.0001
			stop = self.low - self.low * 0.0001 - 0.5 * self.atr0[-1]
			profit_target = entry + abs(entry - stop) * self.vars["RR"]

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
			entry = self.low - self.low * 0.0001
			stop = self.high + 0.5 * self.atr0[-1]
			profit_target = entry - abs(entry - stop) * self.vars["RR"]
		else:
			entry = self.high + self.high * 0.0001
			stop = self.high + self.high * 0.0001 + 0.5 * self.atr0[-1]
			profit_target = entry - abs(entry - stop) * self.vars["RR"]

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

	def after(self):
		self.log(f"W%R is: {self.wPr[-1]}")