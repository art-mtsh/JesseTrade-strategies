from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class Strat17_InsideBar(Strategy):

	# --- HYPERPARAMETERS

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		# body/shadow ratio
		self.vars["bsRatio"] = 50

		# Risk/Reward
		self.vars["RR"] = 1

		# Size of bar inside
		self.vars["inb"] = 0.9

		# Start balance
		self.vars["sb"] = 1000

		# Straight trading / reverse trading
		self.vars["main"] = 1

	# --- INDICATORS ---

	@property
	def ema1(self):
		return ta.ema(self.candles, 20)

	# --- FILTERS ---

	# фільтр body/range
	def bodyToRange(self):
		c_open = self.candles[:, 1]
		c_close = self.candles[:, 2]
		c_high = self.candles[:, 3]
		c_low = self.candles[:, 4]

		return abs(c_open[-1] - c_close[-1]) / (abs(c_high[-1] - c_low[-1]) / 100) > self.vars["bsRatio"] and \
			   abs(c_open[-2] - c_close[-2]) / (abs(c_high[-2] - c_low[-2]) / 100) > self.vars["bsRatio"]

	# фільтр insidebar
	def insideBar(self):
		c_high = self.candles[:, 3]
		c_low = self.candles[:, 4]

		return abs(c_high[-2] - c_low[-2]) * self.vars["inb"] >= abs(c_high[-1] - c_low[-1]) and \
			   c_high[-2] >= c_high[-1] and c_low[-2] <= c_low[-1]

	# фільтр об'єму
	def volFilter(self):
		c_vol = self.candles[:, 5]

		return c_vol[-3] < c_vol[-2] < c_vol[-1]

	# сума всіх фільтрів
	def filters(self):
		return [self.bodyToRange, self.insideBar, self.volFilter]

	# --- DECISION MAKERS ---

	def should_long(self) -> bool:
		c_open = self.candles[:, 1]
		c_close = self.candles[:, 2]

		if self.vars["main"] == 1:
			return c_open[-2] < c_close[-2] and c_open[-1] > c_close[-1] and c_open[-2] > self.ema1
		else:
			return c_open[-2] > c_close[-2] and c_open[-1] < c_close[-1] and c_open[-2] < self.ema1

	def should_short(self) -> bool:
		c_open = self.candles[:, 1]
		c_close = self.candles[:, 2]

		if self.vars["main"] == 1:
			return c_open[-2] > c_close[-2] and c_open[-1] < c_close[-1] and c_open[-2] < self.ema1
		else:
			return c_open[-2] < c_close[-2] and c_open[-1] > c_close[-1] and c_open[-2] > self.ema1


	def should_cancel_entry(self) -> bool:
		return True

	# --- ORDERS ---

	def go_long(self):

		if self.vars["main"] == 1:
			entry = self.high
			stop = self.low - self.low * 0.001
			profit_target = entry + self.vars["RR"] * abs(entry - stop)
		else:
			entry = self.low
			profit_target = self.high + self.high * 0.001
			stop = entry - self.vars["RR"] * abs(entry - profit_target)

		slPercent = abs(stop - entry) / (self.close / 100)
		qty = (self.vars["sb"] / slPercent) / self.close
		self.buy = qty, entry
		self.stop_loss = qty, stop
		self.take_profit = qty, profit_target

	def go_short(self):
		if self.vars["main"] == 1:
			entry = self.low
			stop = self.high + self.high * 0.001
			profit_target = entry - self.vars["RR"] * abs(stop - entry)
		else:
			entry = self.high
			profit_target = self.low - self.low * 0.001
			stop = entry + self.vars["RR"] * abs(entry - profit_target)

		slPercent = abs(stop - entry) / (self.close / 100)
		qty = (self.vars["sb"] / slPercent) / self.close
		self.sell = qty, entry
		self.stop_loss = qty, stop
		self.take_profit = qty, profit_target

