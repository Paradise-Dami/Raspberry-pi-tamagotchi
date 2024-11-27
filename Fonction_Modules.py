import RPi.GPIO as GPIO
import time

class buzzer:
    def __init__(self, pin, freq):
        self.BuzzerPin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BuzzerPin,GPIO.OUT)
        self.buzz = GPIO.PWM(self.BuzzerPin,freq)
    def buzz_start(self, dc):
        self.buzz.start(dc)
    def buzz_stop(self):
        self.buzz.stop()

class button:
    def __init__(self, pin):
        from grove.grove_button import GroveButton
        self.button = GroveButton(pin)
        self.buzz1 = buzzer(22,100)
        def on_press(t):
            self.buzz1.buzz_start(1)
        def on_release(t):
            self.buzz1.buzz_stop()
        self.button.on_press = on_press
        self.button.on_release = on_release

button1 = button(5)

