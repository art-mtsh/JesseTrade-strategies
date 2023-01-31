 # Стратегія Inside Bar
 
Точка прийняття рішень в стратегії - екстремум батьківського бара.

Є функція **розвороту**.

Є фільтри по:   тіло/рендж, 
                r/r, 
                рендж внутрішнього до зовнішнього.


Тести проводились на Н1, М30, М15, М5.

Найкращий результат за пів року на М30:



З такими параметрами:

body/shadow ratio:

self.vars["bsRatio"] = 50

Risk/Reward:

self.vars["RR"] = 1

Size of bar inside:

self.vars["inb"] = 0.9

Start balance:

self.vars["sb"] = 1000

Straight trading / reverse trading:

self.vars["main"] = 1