from pyb import Timer, Pin, delay

TIM3 = Timer(3, freq=20000)
# Motor 1
IN1 = TIM3.channel(1, mode=Timer.PWM, pin=Pin.cpu.B4)
IN2 = TIM3.channel(2, mode=Timer.PWM, pin=Pin.cpu.B5)
# Motor 2
IN3 = TIM3.channel(3, mode=Timer.PWM, pin=Pin.cpu.B0)
IN4 = TIM3.channel(4, mode=Timer.PWM, pin=Pin.cpu.B1)
# Encoder 1
TIM4 = Timer(4, period=0xFFFF, prescaler=0)
TIM4.channel(1, mode=Timer.ENC_AB, pin=Pin.cpu.B6)
TIM4.channel(2, mode=Timer.ENC_AB, pin=Pin.cpu.B7)
# Encoder 2
TIM8 = Timer(8, period=0xFFFF, prescaler=0)
TIM8.channel(1, mode=Timer.ENC_AB, pin=Pin.cpu.C6)
TIM8.channel(2, mode=Timer.ENC_AB, pin=Pin.cpu.C7)


EN = Pin(Pin.cpu.A15, mode=Pin.OUT_PP, value=1)

print('Testing Motor 1')
IN1.pulse_width_percent(50)
IN2.pulse_width_percent(0)
delay(500)
IN1.pulse_width_percent(0)
IN2.pulse_width_percent(0)
print("CCW: " + str(TIM4.counter()))
delay(500)
IN1.pulse_width_percent(0)
IN2.pulse_width_percent(50)
delay(500)
IN1.pulse_width_percent(0)
IN2.pulse_width_percent(0)
print("CW: " + str(TIM4.counter()))
delay(500)



print('Testing Motor 2')
IN3.pulse_width_percent(50)
IN4.pulse_width_percent(0)
delay(500)
IN3.pulse_width_percent(0)
IN4.pulse_width_percent(0)
print("CCW: " + str(TIM8.counter()))
delay(500)
IN3.pulse_width_percent(0)
IN4.pulse_width_percent(50)
delay(500)
IN3.pulse_width_percent(0)
IN4.pulse_width_percent(0)
print("CW: " + str(TIM8.counter()))
delay(500)

EN.low()
