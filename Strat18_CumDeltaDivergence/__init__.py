from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

'''
Ідея стратегії в реакції на 10 ЕМА
Покупка/продажа на 1ЕМА,
Стоп на 10ЕМА
Профіт на 1 RR

'''


class Strat18_CumDeltaDivergence(Strategy):
	# globalBuy = 0
	# globalSell = 0
	#
	# def before(self):
	#
	# 	# --- CUMULATIVE DELTA, HIGH, LOW, VOL ARRAYS CALCULATION ---
	#
	# 	ope = self.candles[:, 1]
	# 	close = self.candles[:, 2]
	# 	high = self.candles[:, 3]
	# 	low = self.candles[:, 4]
	# 	volume = self.candles[:, 5]
	#
	# 	cumDeltaPeriod = 51
	#
	# 	cumDeltaValues = []
	# 	deltaValues = []
	# 	highPriceValues = []
	# 	lowPriceValues = []
	# 	volPriceValues = []
	#
	# 	for i in range(cumDeltaPeriod, 0, -1):
	#
	# 		if close[-i] >= ope[-i] and close[-i] - ope[-i] + 2 * (high[-i] - close[-i]) + 2 * (
	# 				ope[-i] - low[-i]) > 0:
	# 			U1 = volume[-i] * (high[-i] - low[-i]) / (
	# 					close[-i] - ope[-i] + 2 * (high[-i] - close[-i]) + 2 * (ope[-i] - low[-i]))
	# 		else:
	# 			U1 = 0.0
	#
	# 		if close[-i] < ope[-i] and ope[-i] - close[-i] + 2 * (high[-i] - ope[-i]) + 2 * (
	# 				close[-i] - low[-i]) > 0:
	# 			D1 = volume[-i] * (high[-i] - low[-i]) / (
	# 					ope[-i] - close[-i] + 2 * (high[-i] - ope[-i]) + 2 * (close[-i] - low[-i]))
	# 		else:
	# 			D1 = 0.0
	#
	# 		if close[-i] >= ope[-i]:
	# 			if cumDeltaValues == []:
	# 				cumDeltaValues.append(int(U1))
	# 				deltaValues.append(int(U1))
	# 			else:
	# 				cumDeltaValues.append(cumDeltaValues[-1] + int(U1))
	# 				deltaValues.append(int(U1))
	#
	# 		elif close[-i] < ope[-i]:
	# 			if cumDeltaValues == []:
	# 				cumDeltaValues.append(-int(D1))
	# 				deltaValues.append(-int(D1))
	# 			else:
	# 				cumDeltaValues.append(cumDeltaValues[-1] - int(D1))
	# 				deltaValues.append(-int(D1))
	#
	# 		highPriceValues.append(high[-i])
	# 		lowPriceValues.append(low[-i])
	# 		volPriceValues.append(int(volume[-i]))
	#
	# 	# --- CUMULATIVE DELTA FRACTAL ---
	#
	# 	atr_volatility = ta.atr(self.candles, 50, sequential=True) / (self.close / 100)
	#
	# 	for i in range(2, cumDeltaPeriod - 5):
	# 		if cumDeltaValues[-i] < cumDeltaValues[-i - 1] < cumDeltaValues[-i - 2] > cumDeltaValues[-i - 3] > \
	# 				cumDeltaValues[-i - 4]:
	# 			if cumDeltaValues[-1] >= cumDeltaValues[-i - 2] and highPriceValues[-1] < highPriceValues[
	# 				-i - 2] and atr_volatility[-1] > 0.2:
	# 				clean = 0
	# 				for b in range(2, i + 2):
	# 					if highPriceValues[-b] >= highPriceValues[-i - 2] or cumDeltaValues[-b] >= cumDeltaValues[
	# 						-i - 2]:
	# 						clean += 1
	# 				if clean == 0:
	# 					self.globalSell += 1
	# 			break
	#
	# 	for i in range(2, cumDeltaPeriod - 5):
	# 		if cumDeltaValues[-i] > cumDeltaValues[-i - 1] > cumDeltaValues[-i - 2] < cumDeltaValues[-i - 3] < \
	# 				cumDeltaValues[-i - 4]:
	# 			if cumDeltaValues[-1] <= cumDeltaValues[-i - 2] and lowPriceValues[-1] > lowPriceValues[-i - 2] and \
	# 					atr_volatility[-1] > 0.2:
	# 				clean = 0
	# 				for b in range(2, i + 2):
	# 					if lowPriceValues[-b] <= lowPriceValues[-i - 2] or cumDeltaValues[-b] <= cumDeltaValues[
	# 						-i - 2]:
	# 						clean += 1
	# 				if clean == 0:
	# 					self.globalBuy += 1
	# 			break

	# --- HYPERPARAMETERS

	# --- CUSTOM VARIABLES ---

	def __init__(self):
		super().__init__()

		# Start BALANCE
		self.vars["start_bal"] = 100
		# Risk/Reward
		self.vars["RR"] = 0.5

	# --- INDICATORS ---

	# --- FILTERS ---

	# --- ORDERS ---

	def should_long(self) -> bool:
		# --- CUMULATIVE DELTA, HIGH, LOW, VOL ARRAYS CALCULATION ---

		ope = self.candles[:, 1]
		close = self.candles[:, 2]
		high = self.candles[:, 3]
		low = self.candles[:, 4]
		volume = self.candles[:, 5]

		cumDeltaPeriod = 51

		cumDeltaValues = []
		deltaValues = []
		highPriceValues = []
		lowPriceValues = []
		volPriceValues = []

		for i in range(cumDeltaPeriod, 0, -1):

			if close[-i] >= ope[-i] and close[-i] - ope[-i] + 2 * (high[-i] - close[-i]) + 2 * (ope[-i] - low[-i]) > 0:
				U1 = volume[-i] * (high[-i] - low[-i]) / (
						close[-i] - ope[-i] + 2 * (high[-i] - close[-i]) + 2 * (ope[-i] - low[-i]))
			else:
				U1 = 0.0

			if close[-i] < ope[-i] and ope[-i] - close[-i] + 2 * (high[-i] - ope[-i]) + 2 * (close[-i] - low[-i]) > 0:
				D1 = volume[-i] * (high[-i] - low[-i]) / (
						ope[-i] - close[-i] + 2 * (high[-i] - ope[-i]) + 2 * (close[-i] - low[-i]))
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
			lowPriceValues.append(low[-i])
			volPriceValues.append(int(volume[-i]))

		# --- CUMULATIVE DELTA FRACTAL ---

		atr_volatility = ta.atr(self.candles, 50, sequential=True) / (self.close / 100)

		for i in range(2, cumDeltaPeriod - 5):
			if cumDeltaValues[-i] > cumDeltaValues[-i - 1] > cumDeltaValues[-i - 2] < cumDeltaValues[-i - 3] < cumDeltaValues[-i - 4]:
				if cumDeltaValues[-1] <= cumDeltaValues[-i - 2] and lowPriceValues[-1] > lowPriceValues[-i - 2] and atr_volatility[-1] > 0.2:
					clean = 0
					for b in range(2, i + 2):
						if lowPriceValues[-b] <= lowPriceValues[-i - 2] or cumDeltaValues[-b] <= cumDeltaValues[-i - 2]:
							clean += 1
					if clean == 0:
						self.log(f"BULLish divergence on {self.symbol}, with prev. volume {int(volume[-1])}")
						self.log(f"CD fractal on volumes: {volPriceValues[-1]} <= {volPriceValues[-i-2]}")
						self.log(f"HIGHes on fractals: {highPriceValues[-1]} > {highPriceValues[-i-2]}")
						return True
				break


	def should_short(self) -> bool:
		# --- CUMULATIVE DELTA, HIGH, LOW, VOL ARRAYS CALCULATION ---

		ope = self.candles[:, 1]
		close = self.candles[:, 2]
		high = self.candles[:, 3]
		low = self.candles[:, 4]
		volume = self.candles[:, 5]

		cumDeltaPeriod = 51

		cumDeltaValues = []
		deltaValues = []
		highPriceValues = []
		lowPriceValues = []
		volPriceValues = []

		for i in range(cumDeltaPeriod, 0, -1):

			if close[-i] >= ope[-i] and close[-i] - ope[-i] + 2 * (high[-i] - close[-i]) + 2 * (
					ope[-i] - low[-i]) > 0:
				U1 = volume[-i] * (high[-i] - low[-i]) / (
						close[-i] - ope[-i] + 2 * (high[-i] - close[-i]) + 2 * (ope[-i] - low[-i]))
			else:
				U1 = 0.0

			if close[-i] < ope[-i] and ope[-i] - close[-i] + 2 * (high[-i] - ope[-i]) + 2 * (
					close[-i] - low[-i]) > 0:
				D1 = volume[-i] * (high[-i] - low[-i]) / (
						ope[-i] - close[-i] + 2 * (high[-i] - ope[-i]) + 2 * (close[-i] - low[-i]))
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
			lowPriceValues.append(low[-i])
			volPriceValues.append(int(volume[-i]))

		# --- CUMULATIVE DELTA FRACTAL ---

		atr_volatility = ta.atr(self.candles, 50, sequential=True) / (self.close / 100)

		for i in range(2, cumDeltaPeriod - 5):
			if cumDeltaValues[-i] < cumDeltaValues[-i - 1] < cumDeltaValues[-i - 2] > cumDeltaValues[-i - 3] > cumDeltaValues[-i - 4]:
				if cumDeltaValues[-1] >= cumDeltaValues[-i - 2] and highPriceValues[-1] < highPriceValues[-i - 2] and atr_volatility[-1] > 0.2:
					clean = 0
					for b in range(2, i + 2):
						if highPriceValues[-b] >= highPriceValues[-i - 2] or cumDeltaValues[-b] >= cumDeltaValues[-i - 2]:
							clean += 1
					if clean == 0:
						self.log(f"BEARish divergence on {self.symbol}, with prev. volume {int(volume[-1])}")
						self.log(f"CD fractal on volumes: {volPriceValues[-1]} >= {volPriceValues[-i-2]}")
						self.log(f"HIGHes on fractals: {highPriceValues[-1]} < {highPriceValues[-i-2]}")
						return True

				break


	def should_cancel_entry(self) -> bool:
		return True

	def go_long(self):
		high = self.candles[:, 3]
		low = self.candles[:, 4]

		entry = high[-1] + high[-1] * 0.0001
		stop = low[-1] - low[-1] * 0.0001
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
		high = self.candles[:, 3]
		low = self.candles[:, 4]

		entry = low[-1] - low[-1] * 0.0001
		stop = high[-1] + high[-1] * 0.0001
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