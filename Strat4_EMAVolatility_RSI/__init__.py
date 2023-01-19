from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class Strat4_EMAVolatility_RSI(Strategy):

	# --- HYPERPARAMETERS

	def hyperparameters(self):
		return [
			{'name': 'ema1_opt', 'type': int, 'min': 100, 'max': 310, 'default': 300},
			{'name': 'ema2_opt', 'type': int, 'min': 400, 'max': 610, 'default': 600}
			# {'name': 'rsi_opt', 'type': int, 'min': 8, 'max': 25, 'default': 10},
			# {'name': 'rsi_upper', 'type': int, 'min': 60, 'max': 90, 'default': 75},
			# {'name': 'rsi_lower', 'type': int, 'min': 10, 'max': 40, 'default': 25}
		]


	# --- INDICATORS ---

	@property
	def ema1(self):
		return ta.ema(self.candles, self.hp['ema1_opt'], sequential=True)

	@property
	def ema2(self):
		return ta.ema(self.candles, self.hp['ema2_opt'], sequential=True)

	@property
	def rsi3(self):
		return ta.rsi(self.candles, 10)

	# --- FILTERS ---

	def highVolatility(self):
		perc = abs((self.ema1[-1] - self.ema2[-1]) / (self.ema1[-1] / 100))
		return perc > 1

	def filters(self):
		return [self.highVolatility]

	# --- ORDERS ---

	def should_long(self) -> bool:
		return self.rsi3 < 25 and self.ema1[-1] > self.ema2[-1]

	def should_short(self) -> bool:
		return self.rsi3 > 75 and self.ema1[-1] < self.ema2[-1]

	def should_cancel_entry(self) -> bool:
		return False

	def go_long(self):
		entry = self.price

	# 	StopLoss = 2x ATR
		stop = entry - 4 * ta.atr(self.candles)

	# 	TakeProfit = 5x ATR
		profit_target = entry + 8 * ta.atr(self.candles)

	# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

	# 	Buy action
		self.buy = qty, entry

	# 	StopLoss setting
		self.stop_loss = qty, stop

	# 	TakeProfit setting
		self.take_profit = qty, profit_target


	def go_short(self):
		entry = self.price

		# 	StopLoss = 2x ATR
		stop = entry + 4 * ta.atr(self.candles)

		# 	TakeProfit = 5x ATR
		profit_target = entry - 8 * ta.atr(self.candles)

		# 	Quantity to buy, using 3% risk of total account balance
		qty = utils.risk_to_qty(self.balance, 3, entry, stop, self.fee_rate)

		# 	Buy action
		self.sell = qty, entry

		# 	StopLoss setting
		self.stop_loss = qty, stop

		# 	TakeProfit setting
		self.take_profit = qty, profit_target

	# def update_position(self):
	# 	if self.is_long and self.rsi > 75:
	# 		self.liquidate()
	#
	# 	elif self.is_long and self.rsi > 25:
	# 		self.liquidate()
