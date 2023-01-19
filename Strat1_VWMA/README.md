# Стратегія VWMA

Дві VWMA як фільтр і RSI як сигнал для входу.

ATR як ТП/СЛ, або динамічний вихад по протилежному RSI

Тести проводились на М5 та М15

def __init__(self):
  super().__init__()

  self.vars["max_vol_percent"] = 2
  self.vars["min_vol_percent"] = 1
  self.vars["rsi"] = 10
  self.vars["lower_rsi"] = 25
  self.vars["upper_rsi"] = 75
  self.vars["atr_multiplyer"] = 2

![res](https://user-images.githubusercontent.com/108072766/213503555-d29cbe73-4b12-44b1-bcd7-24f71da17448.jpg)
