import RPi.GPIO as GPIO
from grove.grove_button import GroveButton
import time

button = GroveButton(22)
BuzzerPin = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(BuzzerPin,GPIO.OUT)
buzz = GPIO.PWM(BuzzerPin,100)

GPIO.setup(22,GPIO.IN)

octave3 = [261.1,293.7,329.6,349.2,392,440,493.9]
octave3 = []
for freq in octave3:
    buzz = GPIO.PWM(BuzzerPin,freq)
    buzz.start(1)
    time.sleep(0.1)
    buzz.stop()
    time.sleep(0.1)

flouze = 0
def on_press(t):
    global flouze
    flouze += 1
    print("Vous avez",flouze,"grammes de fentanyl dans votre sang.")
    buzz.start(10)
    time.sleep(0.01)
    buzz.stop()
def on_release(t):
    return

button.on_press = on_press
button.on_release = on_release




