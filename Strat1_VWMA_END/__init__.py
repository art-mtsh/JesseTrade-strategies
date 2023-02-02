from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

'''
Короче класика:
фільтр тренду - три ЕМА
decision maker - RSI

проблема як завжди:
- якщо мало трейдів, то мала вибірка і форвард тест провалюється
- якщо багато трейдів, то комісія все від'їдає

'''

class Strat1_VWMA_END(Strategy):

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		# MA1
		self.vars["ma1"] = 60
		# MA2
		self.vars["ma2"] = 150
		# MA3
		self.vars["ma3"] = 180

		# Risk/Reward
		self.vars["RR"] = 1
		# RSI period
		self.vars["rsi"] = 5
		# MIN border RSI
		self.vars["lower_rsi"] = 30
		# MAX border RSI
		self.vars["upper_rsi"] = 70

		# Last bar range
		self.vars["vol_filter"] = 0.7
		# ATR multiplier
		self.vars["atr_multiplyer"] = 2

		# Start balance
		self.vars["start_bal"] = 100

		# reverse? 1=no, 2=yes
		self.vars["REVERSE"] = 1

	# --- INDICATORS ---

	@property
	def ma1(self):
		return ta.wma(self.candles, self.vars["ma1"])

	@property
	def ma2(self):
		return ta.wma(self.candles, self.vars["ma2"])

	@property
	def ma3(self):
		return ta.wma(self.candles, self.vars["ma3"])

	@property
	def rsi(self):
		return ta.rsi(self.candles, self.vars["rsi"])

	# --- FILTERS ---

	# фільтр ренджу останнього бару
	def percent(self):
		return (self.vars["atr_multiplyer"] * ta.atr(self.candles, 100)) / (self.close / 100) > self.vars["vol_filter"]

	# сума всіх фільтрів
	def filters(self):
		return [self.percent]

	# --- ORDERS ---

	def should_long(self) -> bool:

		if self.vars["REVERSE"] == 1:
			return self.low > self.ma1 > self.ma2 > self.ma3 and self.rsi < self.vars["lower_rsi"]
		else:
			return self.high < self.ma1 < self.ma2 < self.ma3 and self.rsi > self.vars["upper_rsi"]

	def should_short(self) -> bool:

		if self.vars["REVERSE"] == 1:
			return self.high < self.ma1 < self.ma2 < self.ma3 and self.rsi > self.vars["upper_rsi"]
		else:
			return self.low > self.ma1 > self.ma2 > self.ma3 and self.rsi < self.vars["lower_rsi"]

	def should_cancel_entry(self) -> bool:
		return False

	def go_long(self):
		if self.vars["REVERSE"] == 1:
			entry = self.close
			stop = entry - self.vars["atr_multiplyer"] * ta.atr(self.candles, 100)
			profit_target = entry + self.vars["RR"] * abs(entry - stop)

		else:
			entry = self.close
			stop = entry - self.vars["atr_multiplyer"] * ta.atr(self.candles, 100)
			profit_target = entry + self.vars["RR"] * abs(entry - stop)

		# StopLoss percent
		slPercent = abs(stop - entry) / (self.close / 100)

		# 	Quantity to buy
		qty = (self.vars["start_bal"] / slPercent) / self.close

		# 	Buy action
		self.buy = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	def go_short(self):
		if self.vars["REVERSE"] == 1:
			entry = self.close
			stop = entry + self.vars["atr_multiplyer"] * ta.atr(self.candles, 100)
			profit_target = entry - self.vars["RR"] * abs(entry - stop)
		else:
			entry = self.close
			stop = entry + self.vars["atr_multiplyer"] * ta.atr(self.candles, 100)
			profit_target = entry - self.vars["RR"] * abs(entry - stop)


		# StopLoss percent
		slPercent = abs(stop - entry) / (self.close / 100)

		# 	Quantity to buy
		qty = (self.vars["start_bal"] / slPercent) / self.close

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target
