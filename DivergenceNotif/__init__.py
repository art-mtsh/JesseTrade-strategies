import datetime

from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils
from datetime import datetime


class DivergenceNotif(Strategy):
	'''
	def before(self):
		ope = self.candles[:, 1]
		close = self.candles[:, 2]
		high = self.candles[:, 3]
		low = self.candles[:, 4]
		volume = self.candles[:, 5]

		cumDeltaPeriod = 51

		cumDeltaValues = []
		deltaValues = []
		highPriceValues = []
		volPriceValues = []

		for i in range(cumDeltaPeriod, 0, -1):

			if close[-i] >= ope[-i] and close[-i] - ope[-i] + 2 * (high[-i] - close[-i]) + 2 * (ope[-i] - low[-i]) > 0:
				U1 = volume[-i] * (high[-i] - low[-i]) / (close[-i] - ope[-i] + 2 * (high[-i] - close[-i]) + 2 * (ope[-i] - low[-i]))
			else:
				U1 = 0.0

			if close[-i] < ope[-i] and ope[-i] - close[-i] + 2 * (high[-i] - ope[-i]) + 2 * (close[-i] - low[-i]) > 0:
				D1 = volume[-i] * (high[-i] - low[-i]) / (ope[-i] - close[-i] + 2 * (high[-i] - ope[-i]) + 2 * (close[-i] - low[-i]))
			else:
				D1 = 0.0

			if close[-i] >= ope[-i]:
				if cumDeltaValues == []:
					cumDeltaValues.append(int(U1))
					deltaValues.append(int(U1))
				else:
					cumDeltaValues.append(cumDeltaValues[-1] + int(U1))
					deltaValues.append(int(U1))

			elif close[-i] < ope[-i]:
				if cumDeltaValues == []:
					cumDeltaValues.append(-int(D1))
					deltaValues.append(-int(D1))
				else:
					cumDeltaValues.append(cumDeltaValues[-1] - int(D1))
					deltaValues.append(-int(D1))

			highPriceValues.append(high[-i])
			volPriceValues.append(int(volume[-i]))

		# self.log(f"Current volume:____{int(volume[-1])}")
		# self.log(f"Cum delta values:__{cumDeltaValues}")
		# self.log(f"Delta values:______{deltaValues}")
		# self.log(f"High price values:_{highPriceValues}")
		# self.log(f"Volume values:_____{volPriceValues}")
		# self.log(f"____________end of hour____________")

		# --- CUMULATIVE DELTA FRACTAL ---

		atr_volatility = ta.atr(self.candles, 50, sequential=True) / (self.close / 100)

		for i in range(2, cumDeltaPeriod-5):
			if cumDeltaValues[-i] < cumDeltaValues[-i-1] < cumDeltaValues[-i-2] > cumDeltaValues[-i-3] > cumDeltaValues[-i-4]:
				if cumDeltaValues[-1] >= cumDeltaValues[-i-2] and highPriceValues[-1] < highPriceValues[-i-2] and atr_volatility[-1] > 0.2:
					clean = 0
					for b in range(2, i+2):
						if highPriceValues[-b] >= highPriceValues[-i-2] or cumDeltaValues[-b] >= highPriceValues[-i-2]:
							clean += 1
					if clean == 0:

						# self.log(f"CD fractal on volumes: {volPriceValues[-1]} >= {volPriceValues[-i-2]}")
						# self.log(f"HIGHes on fractals: {highPriceValues[-1]} < {highPriceValues[-i-2]}")
						self.log(f"Divergence on {self.symbol}, with prev. volume {int(volume[-1])}")
				break
	'''

	def should_long(self) -> bool:
		return False

	def should_short(self) -> bool:
		return False

	def should_cancel_entry(self) -> bool:
		return False

	def go_long(self):
		pass

	def go_short(self):
		pass

	def after(self):
		if ta.ema(self.candles, 10, sequential=False) > ta.ema(self.candles, 20, sequential=False):
			self.log(f"Ema bullish on {self.symbol}")
		else:
			self.log(f"Ema bearish on {self.symbol}")